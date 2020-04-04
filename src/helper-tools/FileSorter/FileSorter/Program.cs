using Microsoft.Extensions.Configuration;
using System;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.IO;
using System.Linq;

namespace FileSorter
{
    class Config
    {
        public string WorkingDir { get; set; }
        public string CombinedDir { get; set; }
    }

    class Program
    {
        static Config Config = new Config();

        static void Configure()
        {
            var config = new ConfigurationBuilder()
                .AddJsonFile("appsettings.json", false, false)
                .Build();
            Config.WorkingDir = string.Format(config[nameof(Config.WorkingDir)], Path.DirectorySeparatorChar);
            Config.CombinedDir = string.Format(config[nameof(Config.CombinedDir)], Path.DirectorySeparatorChar);
        }   

        static void Main(string[] args)
        {
            Configure();
            //Console.WriteLine($"Working directory from configuration {WorkingDir ?? "null" 
            var dirs = Directory.EnumerateDirectories(Config.WorkingDir).Select(x => x.Split(Path.DirectorySeparatorChar).Last().Trim());
            Dictionary<string, List<string>> files = new Dictionary<string, List<string>>();


            foreach (var dir in dirs)
            {
                files.Add(dir, Directory.EnumerateFiles(Path.Combine(Config.WorkingDir, dir)).ToList());
            }

            if (!Directory.Exists(Config.CombinedDir))
            {
                Directory.CreateDirectory(Config.CombinedDir);
            }
            decimal count = files.SelectMany(x => x.Value).LongCount();
            var i = 0m;
            foreach (var file in files.SelectMany(x => x.Value))
            {
                var newFileName = Config.CombinedDir + Path.DirectorySeparatorChar + file.Split(Path.DirectorySeparatorChar).Last();
                if (!File.Exists(newFileName))
                {
                    File.Copy(file, newFileName);
                    Console.WriteLine($"Copying {newFileName.Split(Path.DirectorySeparatorChar).Last()}");
                }
                else
                {
                    Console.WriteLine($"File {newFileName} already exists!");
                }
                i++;
                if (i % 20 == 0)
                {
                    Console.Title = $"Copying...{(i / count)*100}%";
                }
            }

            Console.WriteLine(files.SelectMany(x => x.Value).ToArray().Count());


            //Console.WriteLine(string.Join(',', dirs));

            Console.ReadKey();
        }
    }
}
