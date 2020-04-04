namespace PickupImagesApp
{
    partial class MainForm
    {
        /// <summary>
        ///  Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        ///  Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        ///  Required method for Designer support - do not modify
        ///  the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.pictureBox = new System.Windows.Forms.PictureBox();
            this.chooseInputFolderButton = new System.Windows.Forms.Button();
            this.chooseOutputFolderButton = new System.Windows.Forms.Button();
            this.filesListBox = new System.Windows.Forms.CheckedListBox();
            this.startCopyButton = new System.Windows.Forms.Button();
            this.progressBar = new System.Windows.Forms.ProgressBar();
            this.progressLabel = new System.Windows.Forms.Label();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox)).BeginInit();
            // 
            // pictureBox
            // 
            this.pictureBox.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.pictureBox.Location = new System.Drawing.Point(367, 18);
            this.pictureBox.Name = "pictureBox";
            this.pictureBox.Size = new System.Drawing.Size(497, 500);
            this.pictureBox.SizeMode = System.Windows.Forms.PictureBoxSizeMode.Zoom;
            this.pictureBox.TabIndex = 0;
            this.pictureBox.TabStop = false;
            // 
            // chooseInputFolderButton
            // 
            this.chooseInputFolderButton.Location = new System.Drawing.Point(20, 489);
            this.chooseInputFolderButton.Name = "chooseInputFolderButton";
            this.chooseInputFolderButton.Size = new System.Drawing.Size(94, 29);
            this.chooseInputFolderButton.TabIndex = 1;
            this.chooseInputFolderButton.Text = "Input";
            this.chooseInputFolderButton.UseVisualStyleBackColor = true;
            this.chooseInputFolderButton.Click += new System.EventHandler(this.chooseInputFolderButton_Click);
            // 
            // chooseOutputFolderButton
            // 
            this.chooseOutputFolderButton.Location = new System.Drawing.Point(134, 489);
            this.chooseOutputFolderButton.Name = "chooseOutputFolderButton";
            this.chooseOutputFolderButton.Size = new System.Drawing.Size(94, 29);
            this.chooseOutputFolderButton.TabIndex = 2;
            this.chooseOutputFolderButton.Text = "Output";
            this.chooseOutputFolderButton.UseVisualStyleBackColor = true;
            this.chooseOutputFolderButton.Click += new System.EventHandler(this.chooseOutputFolderButton_Click);
            // 
            // filesListBox
            // 
            this.filesListBox.FormattingEnabled = true;
            this.filesListBox.Location = new System.Drawing.Point(20, 18);
            this.filesListBox.Name = "filesListBox";
            this.filesListBox.Size = new System.Drawing.Size(326, 422);
            this.filesListBox.TabIndex = 3;
            this.filesListBox.SelectedIndexChanged += new System.EventHandler(this.filesListBox_SelectedIndexChanged);
            // 
            // startCopyButton
            // 
            this.startCopyButton.Location = new System.Drawing.Point(252, 489);
            this.startCopyButton.Name = "startCopyButton";
            this.startCopyButton.Size = new System.Drawing.Size(94, 29);
            this.startCopyButton.TabIndex = 4;
            this.startCopyButton.Text = "Copy";
            this.startCopyButton.UseVisualStyleBackColor = true;
            this.startCopyButton.Click += new System.EventHandler(this.startCopyButton_Click);
            // 
            // progressBar
            // 
            this.progressBar.Location = new System.Drawing.Point(20, 447);
            this.progressBar.Name = "progressBar";
            this.progressBar.Size = new System.Drawing.Size(326, 29);
            this.progressBar.TabIndex = 5;
            // 
            // progressLabel
            // 
            this.progressLabel.AutoSize = true;
            this.progressLabel.Location = new System.Drawing.Point(105, 498);
            this.progressLabel.Name = "progressLabel";
            this.progressLabel.Size = new System.Drawing.Size(0, 20);
            this.progressLabel.TabIndex = 6;
            // 
            // MainForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(8F, 20F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(878, 537);
            this.Controls.Add(this.progressLabel);
            this.Controls.Add(this.progressBar);
            this.Controls.Add(this.startCopyButton);
            this.Controls.Add(this.filesListBox);
            this.Controls.Add(this.chooseOutputFolderButton);
            this.Controls.Add(this.chooseInputFolderButton);
            this.Controls.Add(this.pictureBox);
            this.Name = "MainForm";
            this.Text = "Pickup images app";
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox)).EndInit();

        }

        #endregion

        private System.Windows.Forms.PictureBox pictureBox;
        private System.Windows.Forms.Button chooseInputFolderButton;
        private System.Windows.Forms.Button chooseOutputFolderButton;
        private System.Windows.Forms.CheckedListBox filesListBox;
        private System.Windows.Forms.Button startCopyButton;
        private System.Windows.Forms.ProgressBar progressBar;
        private System.Windows.Forms.Label progressLabel;
    }
}

