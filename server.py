from flask import Flask
from songs import get_songs
import copy , datetime
import requests
from bs4 import BeautifulSoup


app = Flask(__name__)

hour , minute = datetime.datetime.now().hour , datetime.datetime.now().minute
html_layout = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Music List</title>
    <style>
        body {
            background-color: #222;
            color: white;
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
        }
        .info-wall {
            margin-bottom: 20px;
            padding: 10px;
            border: 1px solid white;
            border-radius: 5px;
        }
        .music-item {
            margin-bottom: 20px;
            padding: 5px;
            border: 1px solid white;
            border-radius: 5px;
            display: flex;
            align-items: center;
        }
        .music-info {
            flex: 1;
            margin-left: 10px;
        }
        .music-item img {
            width: 100px;
            height: 100px;
            border-radius: 5px;
            margin-right: 15px;
        }
        .image-holder {
            width: 100px;
            height: 100px;
            background-color: #555;
            margin-right: 10px;
            border-radius: 5px;
        }
        button {
            background-color: #3e9c5d;
            color: white;
            border: none;
            width: 100px;   
            padding: 15px;
            border-radius: 5px;
            cursor: pointer;
        }
        button:hover {
            background-color: #7ec489;
        }
        .progress-bar {
            width: 100%;
            height: 10px;
            background-color: #444;
            border-radius: 5px;
            overflow: hidden;
            margin-top: 10px;
        }
        .progress {
            height: 100%;
            background-color: #756bff;
            width: 0;
            transition: width 0.1s;
        }
        .volume-control {
            margin: 15px 0;
        }

        .volume-slider {
            width: 100%;
        }
    </style>
</head>
<body>

<div class="info-wall">
    <h2>Music Information</h2>
    <p>!markInfoWall1!</p>
    <p>!markInfoWall2!</p>
</div>

<div class="music-list">
    !mark!
</div>

<script>
    const playButtons = document.querySelectorAll('.play-button');
    let currentAudio = null;

    playButtons.forEach(button => {
        button.addEventListener('click', function () {
            const audioId = this.getAttribute('data-audio');
            const audioElement = document.getElementById(audioId);
            const progressElement = document.getElementById('progress' + audioId.replace('audio', ''));

            if (currentAudio && currentAudio !== audioElement) {
                currentAudio.pause();
                currentAudio.currentTime = 0;
                document.querySelector(`[data-audio="${currentAudio.id}"]`).textContent = 'Play';
                document.getElementById('progress' + currentAudio.id.replace('audio', '')).style.width = '0';
            }

            if (audioElement.paused) {
                audioElement.play();
                this.textContent = 'Stop';
                currentAudio = audioElement;

                const updateProgress = () => {
                    const percentage = (audioElement.currentTime / audioElement.duration) * 100;
                    progressElement.style.width = percentage + '%';
                    if (!audioElement.paused) {
                        requestAnimationFrame(updateProgress);
                    }
                };
                requestAnimationFrame(updateProgress);
            } else {
                audioElement.pause();
                this.textContent = 'Play';
                currentAudio = null;
            }
        });
    });
</script>

</body>
</html>
'''
html_layout=html_layout.replace('!markInfoWall1!',f'This is website about trending tiktok music!')
html_layout=html_layout.replace('!markInfoWall2!',f'Last playlist update was at {hour}:{minute}')

placeholder = '''
<div class="music-item">
        <div class="image-holder">
<img src="!markImageUrl!" alt="">
        </div>
        <div class="music-info">
            <h3><a style="color:#b0ffff;" href="https://www.tiktok.com/music/-!markTTSongUrl!"> !markIndex!.!markTitle!</a></h3>
            <p>@!markAuthor!</p>
            <p>New videos: !markNewVideos! | Total videos: !markTotalVideos!</p>
            <button class="play-button" data-audio="audio!markIndex!">Play</button>
            <div class="progress-bar">
                <div class="progress" id="progress!markIndex!"></div>
            </div>
            <audio id="audio!markIndex!" src="!markAudioUrl!"></audio>
        </div>
    </div>
'''

mark = ''
songs_data = get_songs()
for i,song in enumerate(songs_data):
    placeholder_copy = copy.deepcopy(placeholder)
    placeholder_copy=placeholder_copy.replace('!markTitle!',song['title'])
    placeholder_copy=placeholder_copy.replace('!markAuthor!',song['author'])
    placeholder_copy=placeholder_copy.replace('!markNewVideos!',song['new_videos'])
    placeholder_copy=placeholder_copy.replace('!markTotalVideos!',song['total_videos'])
    placeholder_copy=placeholder_copy.replace('!markAudioUrl!',song['audio_url'])
    placeholder_copy=placeholder_copy.replace('!markImageUrl!',song['image_url'])
    placeholder_copy=placeholder_copy.replace('!markTTSongUrl!',song['tiktok_song_url'])
    placeholder_copy=placeholder_copy.replace('!markIndex!',str(i+1))
    placeholder_copy=placeholder_copy.replace('!markIndex!',str(i+1))
    placeholder_copy=placeholder_copy.replace('!markIndex!',str(i+1))
    placeholder_copy=placeholder_copy.replace('!markIndex!',str(i+1))
    mark += placeholder_copy + '\n'

ind=html_layout.replace('!mark!',mark)

@app.route('/today')
def main():
    return ind

if __name__ == '__main__':
    print("About to run on http://127.0.0.1:5000/today !")
    app.run(port=5000, debug=True)
