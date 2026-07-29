using System;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Win32;
using System.Windows;
using bgrd.Services;
using bgrd.ViewModels;

namespace bgrd;

public partial class App : Application
{
    public IServiceProvider ServiceProvider { get; private set; } = null!;

    private const string RegistryKeyPath = @"HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize";
    private const string RegistryValueName = "AppsUseLightTheme";

    protected override void OnStartup(StartupEventArgs e)
    {
        base.OnStartup(e);

        var services = new ServiceCollection();
        services.AddSingleton<IConfigService, ConfigService>();
        services.AddSingleton<IVoiceService, VoiceService>();
        services.AddTransient<MainViewModel>();
        services.AddTransient<MainWindow>();

        ServiceProvider = services.BuildServiceProvider();

        ApplyInitialTheme();

        var mainWindow = ServiceProvider.GetRequiredService<MainWindow>();
        mainWindow.Show();
    }

    private void ApplyInitialTheme()
    {
        var config = ServiceProvider.GetRequiredService<IConfigService>();
        var savedTheme = config.Get<string>("theme", null);

        if (string.IsNullOrEmpty(savedTheme))
        {
            bool isLight = GetSystemThemeIsLight();
            savedTheme = isLight ? "light" : "dark";
            config.Set("theme", savedTheme);
        }

        ApplyTheme(savedTheme);
    }

    private bool GetSystemThemeIsLight()
    {
        try
        {
            var value = Registry.GetValue(RegistryKeyPath, RegistryValueName, 1);
            return value is int intValue && intValue == 1;
        }
        catch
        {
            return true;
        }
    }

    internal void ApplyTheme(string theme)
    {
        var uri = theme == "dark" ? "Themes/DarkTheme.xaml" : "Themes/LightTheme.xaml";
        var newDict = new ResourceDictionary
        {
            Source = new Uri(uri, UriKind.Relative)
        };

        var merged = Current.Resources.MergedDictionaries;
        if (merged.Count > 0)
            merged.RemoveAt(0);
        merged.Insert(0, newDict);
    }

    protected override void OnExit(ExitEventArgs e)
    {
        (ServiceProvider?.GetService<IVoiceService>() as VoiceService)?.Dispose();
        base.OnExit(e);
    }
}