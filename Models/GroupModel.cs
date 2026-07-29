using CommunityToolkit.Mvvm.ComponentModel;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;

namespace bgrd.Models;

public partial class GroupModel : ObservableObject
{
    [ObservableProperty]
    private string _name;

    [ObservableProperty]
    private string _filePath;

    [ObservableProperty]
    private List<string> _names = new();

    public GroupModel(string name, string filePath)
    {
        Name = name;
        FilePath = filePath;
        LoadNames();
    }

    private void LoadNames()
    {
        if (string.IsNullOrEmpty(FilePath) || !File.Exists(FilePath))
        {
            Names = new List<string>();
            return;
        }

        var lines = File.ReadAllLines(FilePath, Encoding.UTF8);
        Names = lines.Where(line => !string.IsNullOrWhiteSpace(line))
                     .Select(line => line.Trim())
                     .ToList();
    }

    public void Reload() => LoadNames();
}