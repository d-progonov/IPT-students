using System;
using System.IO;

namespace Common
{
    public class Helper
    {
        public static void Execute(Action action, Action<Exception> errorAction, Action finallyAction)
        {
            try
            {
                action();
            }
            catch (Exception e)
            {
                errorAction(e);
            }
            finally
            {
                finallyAction();
            }
        }

        public static void Log(string message, bool isGood = false)
        {
            if (!isGood)
                Console.WriteLine(message);
            else
                LogConsole(message, ConsoleColor.Green);
        }

        public static string GetFullPath(string path) =>
            Path.IsPathRooted(path) ? path : Path.Combine(Environment.CurrentDirectory, path);
        public static void LogConsole(string message, ConsoleColor color = ConsoleColor.White)
        {
            Console.ForegroundColor = color;
            Console.WriteLine($"{DateTimeOffset.Now}: {message}");
            Console.ResetColor();
        }

        public static void Error(string message)
        {
            LogConsole(message, ConsoleColor.Red);
        }
    }
}
