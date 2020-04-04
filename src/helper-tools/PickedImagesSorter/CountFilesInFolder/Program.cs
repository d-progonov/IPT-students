using System;
using System.IO;
using System.Linq;
using Common;

namespace CountFilesInFolder
{
    class GroupModel
    {
        public int Count { get; set; }
        public string Name { get; set; }
        public string FullPath { get; set; }
    }

    class Program
    {
        static void Main(string[] args)
        {
            Helper.Execute(() =>
            {
                if (args.Length != 1)
                {
                    throw new Exception($"Not valid arguments count were provided!");
                }
                else
                {
                    var path = Helper.GetFullPath(args[0]);
                    if (!Directory.Exists(path))
                    {
                        throw new Exception($"Path {path} was not found!");
                    }

                    var result = Directory.EnumerateDirectories(path)
                        .Select(x => new
                        {
                            path = x,
                            files = Directory.EnumerateFiles(x)
                        })
                        .Select(x => new GroupModel
                        {
                            FullPath = x.path,
                            Name = x.path.Split("\\").LastOrDefault(),
                            Count = x.files.Count()
                        })
                        .OrderByDescending(x => x.Count)
                        .ToList();
                    foreach (var group in result)
                    {
                        Helper.LogConsole($"{group.Name} - {group.Count}", group.Count > 10 ? ConsoleColor.Green : ConsoleColor.Yellow);
                    }
                }
            }, (exception) =>
            {
                Helper.LogConsole(exception.ToString(), ConsoleColor.Red);
                Helper.LogConsole($"Usage: CountFilesInFolder.exe <TARGET PATH>", ConsoleColor.Blue);

            }, () =>
            {
                Console.WriteLine("Press Enter to continue...");
                Console.ReadLine();
            });
        }
    }
}
