using System;
using System.Collections.Generic;
using System.Text;

namespace PickupImagesApp
{
    public class FileModel
    {
        public string Name;
        public string FullPath;
        public string NameWithoutNumber;
        public override string ToString() => Name;
    }
}
