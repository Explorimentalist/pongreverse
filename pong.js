// Add these variables at the top of the file
let startTime = Date.now();
let speedIncrementTime = 5000; // 5 seconds
let speedMultiplier = 1.0;

// Add this function
function updateSpeed() {
    let currentTime = Date.now();
    if (currentTime - startTime >= speedIncrementTime) {
        speedMultiplier += 0.5;
        ball1.dx = BALL_SPEED * speedMultiplier * Math.sign(ball1.dx);
        ball1.dy = BALL_SPEED * speedMultiplier * Math.sign(ball1.dy);
        ball2.dx = BALL_SPEED * speedMultiplier * Math.sign(ball2.dx);
        ball2.dy = BALL_SPEED * speedMultiplier * Math.sign(ball2.dy);
        paddleLeft.dy = PADDLE_SPEED * speedMultiplier * Math.sign(paddleLeft.dy);
        paddleRight.dy = PADDLE_SPEED * speedMultiplier * Math.sign(paddleRight.dy);
        startTime = currentTime;
    }
}

// Call updateSpeed in the gameLoop function
function gameLoop() {
    if (!gameOver) {
        updateSpeed();
        updateBallPositions();
        movePaddles();
        
        if (lives1 <= 0 && lives2 <= 0) {
            message = "It's a tie";
            gameOver = true;
            showRestartMessage = true;
        } else if (lives1 <= 0) {
            message = "Player 2 wins";
            gameOver = true;
            showRestartMessage = true;
        } else if (lives2 <= 0) {
            message = "Player 1 wins";
            gameOver = true;
            showRestartMessage = true;
        }
    }

    drawGame();
    requestAnimationFrame(gameLoop);
}

// Update these variables
let lives1 = 3;
let lives2 = 3;

// Update the updateBallPositions function
function updateBallPositions() {
    [ball1, ball2].forEach((ball, index) => {
        ball.x += ball.dx;
        ball.y += ball.dy;

        // Wall collisions
        if (ball.y <= 0 || ball.y + ball.size >= HEIGHT) {
            ball.dy = -ball.dy;
        }

        // Scoring and lives
        if (ball.x <= 0 || ball.x + ball.size >= WIDTH) {
            if (index === 0) lives1--; else lives2--;
            resetBall(ball, index + 1);
            if (ball.x <= 0) score2++; else score1++;
        }

        // Paddle collisions
        if ((ball.x <= paddleLeft.x + paddleLeft.width && ball.y + ball.size >= paddleLeft.y && ball.y <= paddleLeft.y + paddleLeft.height) ||
            (ball.x + ball.size >= paddleRight.x && ball.y + ball.size >= paddleRight.y && ball.y <= paddleRight.y + paddleRight.height)) {
            ball.dx = -ball.dx;
        }
    });
}

function drawGame() {
    // ... existing drawing code ...

    // Draw lives
    for (let i = 0; i < 3; i++) {
        ctx.fillStyle = i < lives1 ? WHITE : GRAY;
        ctx.beginPath();
        ctx.arc(20 + i * 30, 50, 10, 0, Math.PI * 2);
        ctx.fill();

        ctx.fillStyle = i < lives2 ? WHITE : GRAY;
        ctx.beginPath();
        ctx.arc(WIDTH - 90 + i * 30, 50, 10, 0, Math.PI * 2);
        ctx.fill();
    }

    // ... rest of the drawing code ...
}

function resetGame() {
    score1 = 0;
    score2 = 0;
    lives1 = 3;
    lives2 = 3;
    ball1.x = WIDTH / 2 - BALL_SIZE / 2 - 50;
    ball1.y = HEIGHT / 2 - BALL_SIZE / 2;
    ball2.x = WIDTH / 2 - BALL_SIZE / 2 + 50;
    ball2.y = HEIGHT / 2 - BALL_SIZE / 2;
    ball1.dx = BALL_SPEED;
    ball1.dy = 0;
    ball2.dx = -BALL_SPEED;
    ball2.dy = 0;
    gameOver = false;
    message = "";
    showRestartMessage = false;
    speedMultiplier = 1.0;
    startTime = Date.now();
}

// Update the keydown event listener
document.addEventListener('keydown', (event) => {
    if (gameOver && event.key === 'Enter') {
        resetGame();
    } else {
        // ... existing key controls ...
    }
});
