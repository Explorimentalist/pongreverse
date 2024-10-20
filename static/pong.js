  // Set up the canvas and context
  const canvas = document.getElementById('canvas');
  const ctx = canvas.getContext('2d');

  // Constants
  const WIDTH = canvas.width;
  const HEIGHT = canvas.height;
  const BALL_SIZE = 20;
  const BALL_SPEED = 1; // Changed from 5 to 1
  const PADDLE_WIDTH = 10;
  const PADDLE_HEIGHT = 60;
  const PADDLE_SPEED = 1; // Changed from 5 to 1

  // Colors
  const WHITE = "#FFFFFF";
  const BLACK = "#000000";
  const RED = "#FF0000";
  const BLUE = "#0000FF";
  const GRAY = "#808080";

  // Game state
  let ball1 = {
    x: WIDTH / 2 - BALL_SIZE / 2 - 50,
    y: HEIGHT / 2 - BALL_SIZE / 2,
    width: BALL_SIZE,
    height: BALL_SIZE,
    dx: BALL_SPEED,
    dy: 0
  };

  let ball2 = {
    x: WIDTH / 2 - BALL_SIZE / 2 + 50,
    y: HEIGHT / 2 - BALL_SIZE / 2,
    width: BALL_SIZE,
    height: BALL_SIZE,
    dx: -BALL_SPEED,
    dy: 0
  };

  let paddleLeft = {
    x: 10,
    y: HEIGHT / 2 - PADDLE_HEIGHT / 2,
    width: PADDLE_WIDTH,
    height: PADDLE_HEIGHT,
    dy: PADDLE_SPEED
  };

  let paddleRight = {
    x: WIDTH - 20,
    y: HEIGHT / 2 - PADDLE_HEIGHT / 2,
    width: PADDLE_WIDTH,
    height: PADDLE_HEIGHT,
    dy: -PADDLE_SPEED
  };

  let score1 = 0;
  let score2 = 0;
  let lives1 = 3;
  let lives2 = 3;

  let gameOver = false;
  let message = "";
  let showRestartMessage = false;

  // Speed increase variables
  let startTime = Date.now();
  let speedIncrementTime = 5000; // 5 seconds
  let speedMultiplier = 1.0;

  // Add this near the top of the file with other game state variables
  let blinkTimer = 0;
  const BLINK_INTERVAL = 2000; // Blink every 500ms (0.5 seconds)

  function updateGameState(keys) {
    if (gameOver) return;

    // Move paddles
    paddleLeft.y += paddleLeft.dy;
    paddleRight.y += paddleRight.dy;

    // Reverse paddle direction if they hit the edges
    if (paddleLeft.y <= 0 || paddleLeft.y + PADDLE_HEIGHT >= HEIGHT) {
        paddleLeft.dy = -paddleLeft.dy;
    }
    if (paddleRight.y <= 0 || paddleRight.y + PADDLE_HEIGHT >= HEIGHT) {
        paddleRight.dy = -paddleRight.dy;
    }

    // Move balls based on key presses
    if (keys[87]) { // W key
        ball1.dy = -BALL_SPEED * speedMultiplier;
    } else if (keys[83]) { // S key
        ball1.dy = BALL_SPEED * speedMultiplier;
    } else {
        ball1.dy = 0;
    }

    if (keys[38]) { // Up arrow
        ball2.dy = -BALL_SPEED * speedMultiplier;
    } else if (keys[40]) { // Down arrow
        ball2.dy = BALL_SPEED * speedMultiplier;
    } else {
        ball2.dy = 0;
    }

    // Move balls
    ball1.x += ball1.dx;
    ball1.y += ball1.dy;
    ball2.x += ball2.dx;
    ball2.y += ball2.dy;

    // Ball collisions with walls (top and bottom)
    if (ball1.y <= 0) {
        ball1.y = 0;
        ball1.dy = Math.abs(ball1.dy); // Ensure it's moving downwards
    } else if (ball1.y + BALL_SIZE >= HEIGHT) {
        ball1.y = HEIGHT - BALL_SIZE;
        ball1.dy = -Math.abs(ball1.dy); // Ensure it's moving upwards
    }

    if (ball2.y <= 0) {
        ball2.y = 0;
        ball2.dy = Math.abs(ball2.dy); // Ensure it's moving downwards
    } else if (ball2.y + BALL_SIZE >= HEIGHT) {
        ball2.y = HEIGHT - BALL_SIZE;
        ball2.dy = -Math.abs(ball2.dy); // Ensure it's moving upwards
    }

    // Ball collisions with paddles
    if ((ball1.x <= paddleLeft.x + PADDLE_WIDTH && ball1.y + BALL_SIZE >= paddleLeft.y && ball1.y <= paddleLeft.y + PADDLE_HEIGHT) ||
        (ball1.x + BALL_SIZE >= paddleRight.x && ball1.y + BALL_SIZE >= paddleRight.y && ball1.y <= paddleRight.y + PADDLE_HEIGHT)) {
        ball1.dx = -ball1.dx;
    }

    if ((ball2.x <= paddleLeft.x + PADDLE_WIDTH && ball2.y + BALL_SIZE >= paddleLeft.y && ball2.y <= paddleLeft.y + PADDLE_HEIGHT) ||
        (ball2.x + BALL_SIZE >= paddleRight.x && ball2.y + BALL_SIZE >= paddleRight.y && ball2.y <= paddleRight.y + PADDLE_HEIGHT)) {
        ball2.dx = -ball2.dx;
    }

    // Scoring and resetting balls
    if (ball1.x < 0 || ball1.x > WIDTH) {
        lives1--;
        if (ball1.x > WIDTH) {
            score2++;
        } else {
            score1++;
        }
        resetBall(ball1, 1);
    }

    if (ball2.x < 0 || ball2.x > WIDTH) {
        lives2--;
        if (ball2.x > WIDTH) {
            score1++;
        } else {
            score2++;
        }
        resetBall(ball2, 2);
    }

    // Check for game over
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

    // Update speed
    updateSpeed();
  }

  function resetBall(ball, player) {
    ball.y = HEIGHT / 2 - BALL_SIZE / 2;
    if (player === 1) {
        ball.x = WIDTH / 2 - BALL_SIZE / 2 - 50;
        ball.dx = BALL_SPEED * speedMultiplier;
    } else {
        ball.x = WIDTH / 2 - BALL_SIZE / 2 + 50;
        ball.dx = -BALL_SPEED * speedMultiplier;
    }
    ball.dy = 0;
  }

  function updateSpeed() {
    let currentTime = Date.now();
    if (currentTime - startTime >= speedIncrementTime) {
        speedMultiplier += 0.5;
        ball1.dx = Math.sign(ball1.dx) * BALL_SPEED * speedMultiplier;
        ball2.dx = Math.sign(ball2.dx) * BALL_SPEED * speedMultiplier;
        paddleLeft.dy = Math.sign(paddleLeft.dy) * PADDLE_SPEED * speedMultiplier;
        paddleRight.dy = Math.sign(paddleRight.dy) * PADDLE_SPEED * speedMultiplier;
        startTime = currentTime;
    }
  }

  function resetGame() {
    score1 = 0;
    score2 = 0;
    lives1 = 3;
    lives2 = 3;
    resetBall(ball1, 1);
    resetBall(ball2, 2);
    paddleLeft.y = HEIGHT / 2 - PADDLE_HEIGHT / 2;
    paddleRight.y = HEIGHT / 2 - PADDLE_HEIGHT / 2;
    gameOver = false;
    message = "";
    showRestartMessage = false;

    // Reset speed variables to initial values
    speedMultiplier = 1.0; // Reset speed multiplier
    ball1.dx = BALL_SPEED; // Reset ball speed
    ball1.dy = 0; // Reset ball vertical speed
    ball2.dx = -BALL_SPEED; // Reset ball speed
    ball2.dy = 0; // Reset ball vertical speed
    startTime = Date.now(); // Reset the timer

    blinkTimer = 0; // Reset blink timer
  }

  function draw() {
    ctx.fillStyle = BLACK;
    ctx.fillRect(0, 0, WIDTH, HEIGHT);

    // Draw balls as circles
    ctx.fillStyle = RED;
    ctx.beginPath();
    ctx.arc(ball1.x + BALL_SIZE / 2, ball1.y + BALL_SIZE / 2, BALL_SIZE / 2, 0, Math.PI * 2);
    ctx.fill();

    ctx.fillStyle = BLUE;
    ctx.beginPath();
    ctx.arc(ball2.x + BALL_SIZE / 2, ball2.y + BALL_SIZE / 2, BALL_SIZE / 2, 0, Math.PI * 2);
    ctx.fill();

    // Draw paddles
    ctx.fillStyle = WHITE;
    ctx.fillRect(paddleLeft.x, paddleLeft.y, PADDLE_WIDTH, PADDLE_HEIGHT);
    ctx.fillRect(paddleRight.x, paddleRight.y, PADDLE_WIDTH, PADDLE_HEIGHT);

    // Draw player text
    ctx.fillStyle = WHITE;
    ctx.font = "20px Arial";
    ctx.fillText("Player 1", 10, 30); // Player 1 text
    ctx.fillText("Player 2", WIDTH - 100, 30); // Player 2 text

    // Draw lives as hearts
    for (let i = 0; i < 3; i++) {
        drawHeart(ctx, 20 + i * 30, 50, 24, i < lives1 ? RED : GRAY); // Player 1 hearts
        drawHeart(ctx, WIDTH - 90 + i * 30, 50, 24, i < lives2 ? BLUE : GRAY); // Player 2 hearts
    }

    // Draw game over message
    if (gameOver) {
        ctx.fillStyle = WHITE;
        ctx.font = "30px Arial";
        ctx.fillText(message, WIDTH / 2 - 70, HEIGHT / 2);
        
        if (showRestartMessage) {
            ctx.font = "20px Arial";
            // Only show the message if the blink timer is in the first half of the interval
            if (blinkTimer < BLINK_INTERVAL / 2) {
                ctx.fillStyle = "#525252";
                ctx.fillText("Press Enter to restart", WIDTH / 2 - 80, HEIGHT / 2 + 40);
            }
        }
    }
  }

  const keys = new Array(256).fill(false);

  document.addEventListener('keydown', (e) => {
    keys[e.keyCode] = true;
    if (gameOver && e.key === 'Enter') {
        resetGame();
    }
  });

  document.addEventListener('keyup', (e) => {
    keys[e.keyCode] = false;
  });

  function gameLoop() {
    updateGameState(keys);
    draw();

    // Update blink timer
    if (gameOver) {
        blinkTimer = (blinkTimer + 16) % BLINK_INTERVAL; // Assuming 60 FPS (16ms per frame)
    }

    requestAnimationFrame(gameLoop);
  }

  // Start the game
  resetGame();
  gameLoop();

  function drawHeart(ctx, x, y, size, color) {
    ctx.save();
    ctx.translate(x, y);
    ctx.scale(size / 16, size / 16); // Scale to match the desired size
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.moveTo(1.4875, 9.38767);
    ctx.lineTo(7.13438, 14.6595);
    ctx.bezierCurveTo(7.36875, 14.8783, 7.67812, 15.0002, 8, 15.0002);
    ctx.bezierCurveTo(8.32187, 15.0002, 8.63125, 14.8783, 8.86563, 14.6595);
    ctx.lineTo(14.5125, 9.38767);
    ctx.bezierCurveTo(15.4625, 8.50329, 16, 7.26267, 16, 5.96579);
    ctx.lineTo(16, 5.78454);
    ctx.bezierCurveTo(16, 3.60017, 14.4219, 1.73767, 12.2688, 1.37829);
    ctx.bezierCurveTo(10.8438, 1.14079, 9.39375, 1.60642, 8.375, 2.62517);
    ctx.lineTo(8, 3.00017);
    ctx.lineTo(7.625, 2.62517);
    ctx.bezierCurveTo(6.60625, 1.60642, 5.15625, 1.14079, 3.73125, 1.37829);
    ctx.bezierCurveTo(1.57812, 1.73767, 0, 3.60017, 0, 5.78454);
    ctx.lineTo(0, 5.96579);
    ctx.bezierCurveTo(0, 7.26267, 0.5375, 8.50329, 1.4875, 9.38767);
    ctx.closePath();
    ctx.fill();
    ctx.restore();
  }
