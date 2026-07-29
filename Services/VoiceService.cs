using System;
using System.Collections.Generic;
using System.Speech.Synthesis;  // 这行是关键
namespace bgrd.Services;

public class VoiceService : IVoiceService, IDisposable
{
    private readonly SpeechSynthesizer _synth = new();

    public void Speak(IEnumerable<string> names)
    {
        var text = string.Join("，", names);
        _synth.SpeakAsync(text);
    }

    public void Dispose()
    {
        _synth.Dispose();
    }
}