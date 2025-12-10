+++
date = '2025-02-23T11:23:31+05:30'
draft = false
title = 'Adapter Pattern: Bridging the gap between incompatible interfaces'
tags = ['design-patterns']
categories = ['programming']
image = '/images/1_8nYA7mo3pjhJZT1F2nBSOg.png'
+++

<!-- ![The Adapter pattern in c#](/images/1_8nYA7mo3pjhJZT1F2nBSOg.png) -->

**The Adapter pattern** is a structural design pattern that allows two incompatible interfaces to work together by converting the interface of one class into an interface expected by the clients. In other words, it acts as a bridge between two incompatible interfaces, enabling them to communicate with each other.

## Adapters in real world?

For a phone that does not support a 3.5 mm audio jack, you can use a **USB-C to 3.5 mm audio adapter**. The phone has only a USB-C port, so the adapter converts the USB-C connection into a 3.5 mm audio jack, allowing you to use traditional wired headphones with your phone. The adapter bridges the gap between the old headphone interface and the new phone design.

## Key Components of the Adapter Pattern

Before diving into the code example, let’s break down the key components of the Adapter Pattern:

- **Target**: This is the interface that the client expects to work with.
- **Adaptee**: This is the existing interface that needs to be adapted to the target interface.
- **Adapter**: The adapter is the middleman that implements the target interface and translates the requests to the adaptee’s interface. Adapter implements the target interface and have an instance of adaptee.
- **Client**: The client is the code that uses the target interface.

## Example

Let’s say we have a media player which can play audio files in mp3 format. We also have a video player which can play videos on mp4 format.

What if we just want to listen the audio of the mp4 file. But aur media player only supports the mp3 files.

For that we need an adapter which takes mp4 file and convert it into a mp3 file. Then we can use it in the media player.

Let’s implement it programatically.

### The Target Interface: `IMediaPlayer`

```cs
public interface IMediaPlayer
{
 void Play(string audioType, string fileName);
}

// implementation of target
public class AudioPlayer : IMediaPlayer
{
 public void Play(string audioType, string fileName)
 {
    if (audioType == "mp3")
    {
        Console.WriteLine($"Playing mp3 file. Name: {fileName}");
    }
    else
    {
        Console.WriteLine("Unsupported Audio type");
    }
 }
}
```

## The Adaptee Interface: `IVideoPlayer`

```cs
public interface IVideoPlayer
{
    void PlayVideo(string fileName);
}

public class Mp4Player : IVideoPlayer
{
    public void PlayVideo(string fileName)
    {
        Console.WriteLine($"Playing mp4 file. Name: {fileName}");
    }
}
```

## Adaptor

```cs
public class MediaAdapter : IMediaPlayer
{
 private readonly IVideoPlayer _videoPlayer;

    public MediaAdapter(IVideoPlayer videoPlayer)
    {
        _videoPlayer = videoPlayer;
    }

    public void Play(string audioType, string fileName)
    {
        if (audioType == "mp4")
        {
            _videoPlayer.PlayVideo(fileName);
        }
        else
        {
            Console.WriteLine("Unsupported audio type");
        }
    }

}
```

The `MediaAdapter` class is the heart of the Adapter Pattern in this example. It implements the `IMediaPlayer` interface (the target interface) but internally uses an `IVideoPlayer` (the adaptee interface). This allows the `MediaAdapter` to "adapt" the `IVideoPlayer` to be used where an `IMediaPlayer` is expected.

## Client code

```cs
public class MediaPlayerTestDrive
{
    public static void Main()
    {
        // playing music with media player
        Console.WriteLine("Playing audio in media player");
        IMediaPlayer audioPlayer = new AudioPlayer();
        PlayMedia(audioPlayer, "audio1.mp3", "mp3");

        // playing video with video player
        Console.WriteLine("\\nPlaying video in video player");
        IVideoPlayer videoPlayer = new Mp4Player();
        videoPlayer.PlayVideo("video1.mp4");

        // playing video as mp4 audio with media player
        Console.WriteLine("\\nPlaying mp4 file in media player");
        IMediaPlayer mp4Player = new MediaAdapter(new Mp4Player());
        PlayMedia(mp4Player, "file2.mp4", "mp4");
    }

    private static void PlayMedia(IMediaPlayer mediaPlayer, string fileName, string fileType)
    {
        mediaPlayer.Play( fileType, fileName);
    }

}
```

In the `MediaPlayerTestDrive` class, we test different scenarios:

- Playing an MP3 file using the `AudioPlayer`.
- Playing an MP4 video directly using the `Mp4Player`.
- Playing an MP4 file using the `MediaAdapter`, which allows the MP4 video to be played via the `IMediaPlayer` interface.

## Why Use the Adapter Pattern?

The Adapter Pattern is particularly useful when:

- You want to use a class that doesn’t fit the expected interface.
- You need to integrate third-party libraries or legacy code into your system.
- You want to promote code reuse by integrating classes that weren’t initially designed to work together.

## Conclusion

The Adapter Pattern is a powerful tool in a developer’s toolkit, enabling compatibility between incompatible interfaces. In our example, the `MediaAdapter` class allows an `IVideoPlayer` to be used where an `IMediaPlayer` is expected, demonstrating the elegance and simplicity of the Adapter Pattern. This pattern helps in building flexible, maintainable, and reusable code, making it an essential concept to grasp in software design.

If you ever find yourself needing to integrate systems with incompatible interfaces, the Adapter Pattern might just be the solution you’re looking for!

[Canonical link](https://medium.com/@ravindradevrani/adapter-pattern-bridging-the-gap-between-incompatible-interfaces-7c51443a55cf)
