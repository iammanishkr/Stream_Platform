const playPauseButton = document.getElementById('play-pause');
const currentSongTitle = document.getElementById('current-song-title');
const currentSongArtist = document.getElementById('current-song-artist');
const currentSongCover = document.getElementById('current-song-cover');
const progressBar = document.getElementById('progress');
const currentTimeElement = document.getElementById('current-time');
const durationElement = document.getElementById('duration');
let audio = new Audio();
let isPlaying = false;

function formatTime(seconds) {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = Math.floor(seconds % 60);
    return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
}

// Ensure all elements exist before using them
if (playPauseButton && currentSongTitle && currentSongArtist && currentSongCover && progressBar && currentTimeElement && durationElement) {
    document.querySelectorAll('.song-card').forEach(card => {
        card.addEventListener('click', () => {
            const songUrl = card.getAttribute('data-url');
            const songTitle = card.getAttribute('data-title');
            const songArtist = card.getAttribute('data-artist');
            const songCover = card.getAttribute('data-cover');

            // Update audio source and UI even if the same song is clicked
            audio.src = songUrl;
            currentSongTitle.textContent = songTitle;
            currentSongArtist.textContent = songArtist;
            currentSongCover.src = songCover;

            // Play audio with error handling for autoplay issues
            audio.play().then(() => {
                playPauseButton.innerHTML = '<i class="fas fa-pause"></i>';
                isPlaying = true;
            }).catch(error => {
                console.error("Autoplay failed:", error);
            });
        });
    });

    playPauseButton.addEventListener('click', togglePlayPause);

    function togglePlayPause() {
        if (isPlaying) {
            audio.pause();
            playPauseButton.innerHTML = '<i class="fas fa-play"></i>';
        } else {
            audio.play().then(() => {
                playPauseButton.innerHTML = '<i class="fas fa-pause"></i>';
            }).catch(error => {
                console.error("Play failed:", error);
            });
        }
        isPlaying = !isPlaying;
    }

    audio.addEventListener('timeupdate', () => {
        if (!isNaN(audio.duration)) {
            progressBar.value = (audio.currentTime / audio.duration) * 100;
            currentTimeElement.textContent = formatTime(audio.currentTime);
        }
    });

    audio.addEventListener('loadedmetadata', () => {
        durationElement.textContent = formatTime(audio.duration);
    });

    progressBar.addEventListener('input', () => {
        const time = (progressBar.value / 100) * audio.duration;
        if (!isNaN(time)) {
            audio.currentTime = time;
            currentTimeElement.textContent = formatTime(time);
        }
    });

    // Add hover effect to player buttons
    const playerButtons = document.querySelectorAll('.controls button');
    playerButtons.forEach(button => {
        button.addEventListener('mouseover', () => {
            button.style.transform = 'scale(1.1)';
        });
        button.addEventListener('mouseout', () => {
            button.style.transform = 'scale(1)';
        });
    });
} else {
    console.error("One or more player elements are missing from the DOM.");
}
