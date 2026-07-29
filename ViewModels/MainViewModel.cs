using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using bgrd.Models;
using bgrd.Services;
using bgrd.Views;
using System;
using System.Collections.ObjectModel;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using System.Windows;

namespace bgrd.ViewModels;

public partial class MainViewModel : ObservableObject
{
    private readonly IConfigService _configService;
    private readonly IVoiceService _voiceService;
    private readonly App _app;

    [ObservableProperty]
    private ObservableCollection<GroupModel> _groups = new();

    [ObservableProperty]
    private GroupModel? _selectedGroup;

    [ObservableProperty]
    private int _pickCount = 1;

    [ObservableProperty]
    private string _resultText = "📋 选择队列开始点名";

    [ObservableProperty]
    private bool _isPicking;

    public MainViewModel(IConfigService configService, IVoiceService voiceService)
    {
        _configService = configService;
        _voiceService = voiceService;
        _app = (App)Application.Current;

        LoadGroups();
        PickCount = _configService.Get("pick_count", 1);

        if (Groups.Any())
            SelectedGroup = Groups[0];
        else
            ResultText = "⚠️ 未加载任何队列，请手动添加";
    }

    private void LoadGroups()
    {
        var savedGroups = _configService.Get<GroupConfig[]>("groups", null);
        if (savedGroups != null && savedGroups.Length > 0)
        {
            foreach (var g in savedGroups)
                Groups.Add(new GroupModel(g.Name, g.FilePath));
            return;
        }

        ScanAssetsByLevel();
    }

    private void ScanAssetsByLevel()
    {
        var assetsDir = Path.Combine(AppContext.BaseDirectory, "Assets");
        if (!Directory.Exists(assetsDir))
        {
            MessageBox.Show($"Assets 目录不存在，请创建并放置 1.txt",
                            "错误", MessageBoxButton.OK, MessageBoxImage.Error);
            return;
        }

        string filePath = Path.Combine(assetsDir, "1.txt");
        if (File.Exists(filePath))
        {
            Groups.Add(new GroupModel("第1层", filePath));
        }
        else
        {
            MessageBox.Show($"未找到第1层名单文件：1.txt",
                            "层级缺失", MessageBoxButton.OK, MessageBoxImage.Error);
        }

        if (Groups.Count == 0)
        {
            ResultText = "⚠️ 未找到任何层级文件，请手动添加队列";
        }

        SaveGroups();
    }

    private void SaveGroups()
    {
        var configs = Groups.Select(g => new GroupConfig { Name = g.Name, FilePath = g.FilePath }).ToArray();
        _configService.Set("groups", configs);
    }

    [RelayCommand]
    private void AddGroup()
    {
        var dialog = new GroupEditDialog();
        if (dialog.ShowDialog() == true)
        {
            var group = new GroupModel(dialog.GroupName, dialog.FilePath);
            Groups.Add(group);
            SelectedGroup = group;
            SaveGroups();
        }
    }

    [RelayCommand]
    private void RemoveGroup(GroupModel group)
    {
        if (Groups.Count <= 1)
        {
            MessageBox.Show("至少保留一个队列。", "提示", MessageBoxButton.OK, MessageBoxImage.Information);
            return;
        }
        Groups.Remove(group);
        if (SelectedGroup == group)
            SelectedGroup = Groups.FirstOrDefault();
        SaveGroups();
    }

    [RelayCommand]
    private void RefreshGroup()
    {
        SelectedGroup?.Reload();
        SaveGroups();
    }

    [RelayCommand]
    private async Task StartPick()
    {
        if (SelectedGroup == null || SelectedGroup.Names.Count == 0)
        {
            ResultText = "⚠️ 当前队列为空，请添加人员！";
            return;
        }

        int count = Math.Min(PickCount, SelectedGroup.Names.Count);
        if (count != PickCount) PickCount = count;

        IsPicking = true;
        ResultText = "🎯 抽选中...";
        await Task.Delay(2000);

        var random = new Random();
        var selected = SelectedGroup.Names.OrderBy(_ => random.Next()).Take(count).ToList();
        ResultText = string.Join("  ", selected);

        bool voiceEnabled = _configService.Get("voice_enabled", true);
        if (voiceEnabled && selected.Any())
            _voiceService.Speak(selected);

        IsPicking = false;
    }

    [RelayCommand]
    private void ToggleTheme()
    {
        var current = _configService.Get<string>("theme", "light");
        string newTheme = current == "light" ? "dark" : "light";
        _configService.Set("theme", newTheme);
        _app.ApplyTheme(newTheme);
    }

    [RelayCommand]
    private void OpenSettings()
    {
        var current = _configService.Get("voice_enabled", true);
        var result = MessageBox.Show($"当前语音播报: {(current ? "开启" : "关闭")}\n点击确定切换，取消不变。",
                                     "语音设置", MessageBoxButton.OKCancel, MessageBoxImage.Question);
        if (result == MessageBoxResult.OK)
        {
            _configService.Set("voice_enabled", !current);
            MessageBox.Show("已切换语音状态。", "提示", MessageBoxButton.OK, MessageBoxImage.Information);
        }
    }

    partial void OnPickCountChanged(int value)
    {
        _configService.Set("pick_count", value);
    }
}