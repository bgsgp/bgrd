using System.IO;
using System.Windows;
using Microsoft.Win32;

namespace bgrd.Views;

public partial class GroupEditDialog : Window
{
    public string GroupName { get; set; } = string.Empty;
    public string FilePath { get; set; } = string.Empty;

    public GroupEditDialog(string? existingName = null, string? existingPath = null)
    {
        InitializeComponent();
        DataContext = this;
        if (!string.IsNullOrEmpty(existingName)) GroupName = existingName;
        if (!string.IsNullOrEmpty(existingPath)) FilePath = existingPath;
    }

    private void Browse_Click(object sender, RoutedEventArgs e)
    {
        var dlg = new OpenFileDialog
        {
            Filter = "文本文件 (*.txt)|*.txt|所有文件 (*.*)|*.*",
            Title = "选择名单文件"
        };
        if (dlg.ShowDialog() == true)
        {
            FilePath = dlg.FileName;
            if (string.IsNullOrWhiteSpace(GroupName))
                GroupName = Path.GetFileNameWithoutExtension(FilePath);
            DataContext = null;
            DataContext = this;
        }
    }

    private void Ok_Click(object sender, RoutedEventArgs e)
    {
        if (string.IsNullOrWhiteSpace(GroupName))
        {
            MessageBox.Show("请输入队列名称。", "提示", MessageBoxButton.OK, MessageBoxImage.Warning);
            return;
        }
        if (string.IsNullOrWhiteSpace(FilePath) || !File.Exists(FilePath))
        {
            MessageBox.Show("请选择有效的名单文件。", "提示", MessageBoxButton.OK, MessageBoxImage.Warning);
            return;
        }
        DialogResult = true;
        Close();
    }

    private void Cancel_Click(object sender, RoutedEventArgs e)
    {
        DialogResult = false;
        Close();
    }
}