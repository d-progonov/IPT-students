using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace PickupImagesApp
{
    public partial class MainForm : Form
    {
        private string _inputFolder;
        private string _outputFolder;
        public MainForm()
        {
            InitializeComponent();
            startCopyButton.Enabled = chooseOutputFolderButton.Enabled = false;
        }

        private void chooseInputFolderButton_Click(object sender, EventArgs e)
        {
            using var dialog = new FolderBrowserDialog
            {
                Description = "Choose input folder with images",
                UseDescriptionForTitle = true
            };
            if (dialog.ShowDialog(this) == DialogResult.OK)
            {
                var folder = _inputFolder = dialog.SelectedPath;
                var imagesPathsWithNames = Directory.EnumerateFiles(folder, "*.jpg")
                    .Select(x =>
                    {
                        var model = new FileModel
                        {
                            FullPath = x,
                            Name = Path.GetFileNameWithoutExtension(x),
                        };
                        var splitted = model.Name.Split('_');
                        if (splitted.Length == 3)
                        {
                            model.NameWithoutNumber = splitted[0] + splitted[1];
                        }
                        else
                        {
                            model.NameWithoutNumber = null;
                        }
                        return model;
                    });
                var groupedImages = imagesPathsWithNames
                    .Where(x => x.NameWithoutNumber != null)
                    .GroupBy(x => x.NameWithoutNumber)
                    .Where(x => x.Count() > 1)
                    .SelectMany(x => x.AsEnumerable())
                    .ToList();
                filesListBox.DataSource = groupedImages;
                if (groupedImages.Any())
                {
                    chooseOutputFolderButton.Enabled = true;
                }
                return;
            }
            chooseOutputFolderButton.Enabled = false;
        }

        private void filesListBox_SelectedIndexChanged(object sender, EventArgs e)
        {
            if (filesListBox.SelectedItem is FileModel selectedFile)
            {
                pictureBox.ImageLocation = selectedFile.FullPath;
            }
        }

        private void chooseOutputFolderButton_Click(object sender, EventArgs e)
        {
            using var dialog = new FolderBrowserDialog
            {
                Description = "Choose output folder for good images",
                UseDescriptionForTitle = true
            };
            if (dialog.ShowDialog(this) == DialogResult.OK)
            {
                _outputFolder = dialog.SelectedPath;
                startCopyButton.Enabled = true;
            }
            else
            {
                startCopyButton.Enabled = false;
            }
        }

        private void startCopyButton_Click(object sender, EventArgs e)
        {
            try
            {
                chooseInputFolderButton.Visible = chooseOutputFolderButton.Visible = startCopyButton.Visible = false;
                int count = filesListBox.CheckedItems.Count;
                int i = 0;
                progressBar.Maximum = count;
                foreach (var item in filesListBox.CheckedItems)
                {
                    var fileModel = item as FileModel;
                    if (fileModel != null)
                    {
                        File.Copy(fileModel.FullPath, Path.Combine(_outputFolder, fileModel.Name + Path.GetExtension(fileModel.FullPath)));
                    }

                    progressBar.Value = i++;
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.ToString());
            }
            finally
            {
                chooseInputFolderButton.Visible = chooseOutputFolderButton.Visible = startCopyButton.Visible = true;
            }
        }
    }
}
