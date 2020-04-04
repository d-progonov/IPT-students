using System;
using System.IO;
using System.Linq;
using System.Security.Cryptography;
using Common;

namespace PickedImagesSorter
{
    class Program
    {
        static void ValidateAndSetParams(string[] args)
        {
            if (args.Length != 2)
                throw new Exception("Not enough arguments were provided!");
            if (args.Any(string.IsNullOrWhiteSpace))
            {
                throw new Exception("Arguments supported are empty or whitespaces!");
            }
            else
            {
                var input = Helper.GetFullPath(args[0]);
                var output = Helper.GetFullPath(args[1]);
                if (!Directory.Exists(input))
                {
                    throw new Exception($"{input} directory was not found!");
                }

                InputFolder = input;
                OutPutFolder = output;
                if (!Directory.Exists(OutPutFolder))
                {
                    Directory.CreateDirectory(OutPutFolder);
                }
            }
        }

        private static string InputFolder;
        private static string OutPutFolder;

        static void Main(string[] args)
        {
            Helper.Execute(() =>
            {
                ValidateAndSetParams(args);
                SortAndCopyImages();
            }, (ex) =>
            {
                if (!string.IsNullOrWhiteSpace(OutPutFolder))
                {
                    Helper.Execute(() =>
                    {
                        Directory.Delete(OutPutFolder);
                    }, deletEx =>
                    {
                        Helper.Error($"Error while trying to delete {OutPutFolder}: {deletEx.Message}");
                    }, () =>
                    {
                        Helper.Log($"End directory deleting...");
                    });
                }
                Helper.Error(ex.Message);
                Helper.LogConsole("USAGE: PickedImagesSorter.exe <PATH_TO_PICKED_IMAGES> <PATH_TO_STORE_IMAGES>");
            }, () =>
            {
                Console.WriteLine("Press Enter to continue...");
                Console.ReadLine();
            });
        }



        static void SortAndCopyImages()
        {
            Helper.Log("Starting images copy...");
            Helper.Log($"Input path is {InputFolder}");


            var allowedExtensions = new[] {".jpg", ".png", ".jpeg"};
            var images = Directory.EnumerateFiles(InputFolder).ToList();
            Helper.Log($"Files count: {images.Count}");
            images = images
                .Where(x => allowedExtensions.Contains(Path.GetExtension(x))).ToList();
            Helper.Log($"Files with extensions: [{string.Join(',', allowedExtensions)}]: {images.Count}");
            var models = images.Select(x =>
            {
                var model = new FileModel
                {
                    FullPath = x,
                    Name = Path.GetFileNameWithoutExtension(x),
                };
                var splitted = model.Name.Split('_');
                if (splitted.Length == 3)
                {
                    model.NameWithoutNumber = $"{splitted[0]}_{splitted[1]}";
                }
                else
                {
                    model.NameWithoutNumber = null;
                }
                return model;
            });

            var groups = models
                .Where(x => x.NameWithoutNumber != null)
                .GroupBy(x => x.NameWithoutNumber)
                .ToList();
            Helper.Log($"Groups count {groups.Count}");
            foreach (var group in groups)
            {
                var personName = group.Key;
                var count = group.Count();
                Helper.Log($"Person: {personName}, Count: {count}", true);
                if (count > 1)
                {
                    var pathToSave = Path.Combine(OutPutFolder, personName);
                    Helper.Log($"Saving images to {pathToSave}...");
                    Directory.CreateDirectory(pathToSave);
                    foreach (var fileModel in group.AsEnumerable())
                    {
                        Helper.Log($"Copying {fileModel.Name}...");
                        var fileToSave = Path.Combine(pathToSave,
                            fileModel.Name + Path.GetExtension(fileModel.FullPath));
                        File.Copy(fileModel.FullPath, fileToSave);
                    }
                }
                else
                {
                    Helper.Log($"Count in less threshold, skipping this person");
                }

            }

        }
    }
}
