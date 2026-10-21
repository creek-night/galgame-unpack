using System;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Runtime.CompilerServices;
using System.Text;
using System.Web.Script.Serialization;
using System.Windows.Media.Imaging;
using GameRes;
using GameRes.Formats.KiriKiri;

class GarbroBridge {
    static JavaScriptSerializer json = new JavaScriptSerializer { MaxJsonLength = 64 * 1024 * 1024 };
    static string library;
    static string scheme;
    [STAThread]
    static int Main(string[] args) {
        Console.OutputEncoding = new UTF8Encoding(false);
        try {
            var values = args.ToList();
            var si = values.IndexOf("--scheme");
            if(si >= 0) {
                if(si + 2 != values.Count) throw new ArgumentException("--scheme NAME must be the last two arguments");
                scheme = values[si+1];
                values.RemoveRange(si,2);
                args = values.ToArray();
            }
            if(args.Length < 2) throw new ArgumentException("garbro_bridge GARbro schemes|list|image|entry|raw [source] [entry] [output] [--scheme TITLE|NoCrypt]");
            library = Path.GetFullPath(args[0]);
            AppDomain.CurrentDomain.AssemblyResolve += (s,e) => {
                var path = Path.Combine(library, new AssemblyName(e.Name).Name + ".dll");
                return File.Exists(path) ? Assembly.LoadFrom(path) : null;
            };
            return Run(args);
        } catch(Exception e) { Console.Error.WriteLine(e.ToString()); return 1; }
    }
    static void Emit(object value) { Console.WriteLine(json.Serialize(value)); }
    static FileStream CreateOutput(string path) {
        path = Path.GetFullPath(path);
        Directory.CreateDirectory(Path.GetDirectoryName(path));
        return new FileStream(path, FileMode.CreateNew, FileAccess.Write);
    }
    static void SaveImage(ImageData image, string path) {
        if(image == null) throw new InvalidDataException("No supported image decoder");
        var enc = new PngBitmapEncoder();
        enc.Frames.Add(BitmapFrame.Create(image.Bitmap));
        using(var output = CreateOutput(path)) enc.Save(output);
        Emit(new { output = Path.GetFullPath(path), width=image.Width, height=image.Height,
                   offset_x=image.OffsetX, offset_y=image.OffsetY, bpp=image.BPP });
    }
    static bool SaveNativePng(Stream input, string path) {
        if(!input.CanSeek) return false;
        long start = input.Position;
        byte[] signature = new byte[8];
        int read = input.Read(signature,0,8);
        input.Position = start;
        byte[] png = new byte[] {137,80,78,71,13,10,26,10};
        if(read != 8 || !signature.SequenceEqual(png)) return false;
        var decoder = BitmapDecoder.Create(input,BitmapCreateOptions.PreservePixelFormat,BitmapCacheOption.OnLoad);
        var frame = decoder.Frames[0];
        input.Position = start;
        using(var output = CreateOutput(path)) input.CopyTo(output);
        Emit(new { output=Path.GetFullPath(path),width=frame.PixelWidth,height=frame.PixelHeight,
                   offset_x=0,offset_y=0,bpp=frame.Format.BitsPerPixel,encoding="original PNG bytes" });
        return true;
    }
    [MethodImpl(MethodImplOptions.NoInlining)]
    static int Run(string[] a) {
        if(a[1] == "schemes" || (scheme != null && scheme != "NoCrypt")) {
            using(var input = File.OpenRead(Path.Combine(library,"GameData","Formats.dat")))
                FormatCatalog.Instance.DeserializeScheme(input);
        }
        if(a[1] == "schemes") {
            Emit(Xp3Opener.KnownSchemes.Select(kv=>new { title=kv.Key, cipher=kv.Value.GetType().FullName }).ToArray());
            return 0;
        }
        if(scheme != null) {
            if(scheme != "NoCrypt" && !Xp3Opener.KnownSchemes.ContainsKey(scheme))
                throw new ArgumentException("Unknown XP3 scheme: " + scheme);
            ICrypt cipher = scheme == "NoCrypt" ? new NoCrypt() : Xp3Opener.KnownSchemes[scheme];
            FormatCatalog.Instance.ParametersRequest += (sender,e) => {
                e.Options = new Xp3Options { Scheme = cipher };
                e.InputResult = true;
            };
        }
        if(a.Length < 3) throw new ArgumentException("Source path is required");
        if(a[1] == "image") {
            if(a.Length != 4) throw new ArgumentException("image <source> <output.png>");
            using(var native = File.OpenRead(a[2])) { if(SaveNativePng(native,a[3])) return 0; }
            using(var s = BinaryStream.FromFile(a[2])) SaveImage(ImageFormat.Read(s), a[3]);
            return 0;
        }
        using(var arc = ArcFile.TryOpen(a[2])) {
            if(arc == null) throw new InvalidDataException("Archive open failed; inspect the inner error and explicit XP3 scheme", FormatCatalog.Instance.LastError);
            if(a[1] == "list") {
                Emit(new { source=Path.GetFullPath(a[2]), format=arc.Tag, xp3_scheme=scheme,
                    entries=arc.Dir.Select(e => new { name=e.Name, size=e.Size, offset=e.Offset, type=e.Type }).ToArray() });
                return 0;
            }
            if(a.Length != 5) throw new ArgumentException("entry|raw <archive> <exact-entry-name> <output>");
            var entry = arc.Dir.Single(e => e.Name == a[3]);
            if(a[1] == "entry") {
                using(var native = arc.OpenEntry(entry)) { if(SaveNativePng(native,a[4])) return 0; }
                using(var image = arc.OpenImage(entry)) SaveImage(image.Image, a[4]);
            } else if(a[1] == "raw") {
                using(var input = arc.OpenEntry(entry))
                using(var output = CreateOutput(a[4])) input.CopyTo(output);
                Emit(new { output=Path.GetFullPath(a[4]), entry=entry.Name });
            } else throw new ArgumentException("Unknown command");
        }
        return 0;
    }
}
