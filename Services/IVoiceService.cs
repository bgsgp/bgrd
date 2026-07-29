using System.Collections.Generic;

namespace bgrd.Services;

public interface IVoiceService
{
    void Speak(IEnumerable<string> names);
}