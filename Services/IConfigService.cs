namespace bgrd.Services;

public interface IConfigService
{
    T Get<T>(string key, T defaultValue);
    void Set<T>(string key, T value);
    void Save();
}