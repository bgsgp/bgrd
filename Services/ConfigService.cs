using System;
using System.Collections.Generic;
using System.IO;
using System.Text.Json;

namespace bgrd.Services;

public class ConfigService : IConfigService
{
    private readonly string _configPath;
    private Dictionary<string, object> _config;

    public ConfigService()
    {
        var appData = Path.Combine(
            Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData),
            "bgrd");
        Directory.CreateDirectory(appData);
        _configPath = Path.Combine(appData, "config.json");
        _config = LoadConfig();
    }

    private Dictionary<string, object> LoadConfig()
    {
        if (!File.Exists(_configPath))
            return new Dictionary<string, object>();

        try
        {
            var json = File.ReadAllText(_configPath);
            return JsonSerializer.Deserialize<Dictionary<string, object>>(json)
                   ?? new Dictionary<string, object>();
        }
        catch
        {
            return new Dictionary<string, object>();
        }
    }

    public T Get<T>(string key, T defaultValue)
    {
        if (_config.TryGetValue(key, out var value))
        {
            try
            {
                return (T)Convert.ChangeType(value, typeof(T));
            }
            catch
            {
                return defaultValue;
            }
        }
        return defaultValue;
    }

    public void Set<T>(string key, T value)
    {
        _config[key] = value!;
        Save();
    }

    public void Save()
    {
        var json = JsonSerializer.Serialize(_config, new JsonSerializerOptions
        {
            WriteIndented = true
        });
        File.WriteAllText(_configPath, json);
    }
}