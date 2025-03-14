const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const scoreElement = document.getElementById('scoreValue');
const startButton = document.getElementById('startButton');

// 游戏对象
const ball = {
    x: canvas.width / 2,
    y: canvas.height / 2,
    radius: 10,
    speed: 4,
    dx: 4,
    dy: -4,
    color: '#ffffff'
};

const paddle = {
    width: 100,
    height: 10,
    x: canvas.width / 2 - 50,
    y: canvas.height - 20,
    speed: 8,
    dx: 0,
    color: '#4CAF50'
};

let score = 0;
let gameLoop;
let gameStarted = false;
let autoModes = -1;

// 添加血量相关变量
let maxHealth = 100;
let currentHealth = maxHealth;
const healthBar = document.getElementById('healthBar');
const healthLossPerMiss = 20; // 每次失误扣除的血量

// 事件监听器
document.addEventListener('keydown', keyDown);
document.addEventListener('keyup', keyUp);
document.addEventListener('keydown',restartGame);
startButton.addEventListener('click', startGame);

// 控制板子移动
function keyDown(e) {
    if (e.key === 'd' || e.key === 'ArrowRight' || e.key === 'right') {
        paddle.dx = paddle.speed;
    } else if (e.key === 'a' || e.key === 'ArrowLeft' || e.key === 'left') {
        paddle.dx = -paddle.speed;
    } else if (e.key === 't') {
        autoModes *= -1;
    }
}

function keyUp(e) {
    if (
        e.key === 'd' ||
        e.key === 'ArrowRight' ||
        e.key === 'a' ||
        e.key === 'ArrowLeft'
    ) {
        paddle.dx = 0;
    }
}

function restartGame(e) {
    if (e.key === ' ' || e.code === 'Space') {
        startGame();
    }
}

// 开始游戏
function startGame() {
    if (!gameStarted) {
        gameStarted = true;
        startButton.style.display = 'none';
        resetGame();
        gameLoop = setInterval(update, 16); // 约60fps
    }
}

// 重置游戏
function resetGame() {
    score = 0;
    currentHealth = maxHealth;
    updateHealthBar();
    scoreElement.innerHTML = score;
    ball.x = canvas.width / 2;
    ball.y = canvas.height / 2;
    ball.dx = ball.speed;
    ball.dy = -ball.speed;
    paddle.x = canvas.width / 2 - paddle.width / 2;
}

// 添加更新血条函数
function updateHealthBar() {
    healthBar.style.width = (currentHealth / maxHealth * 100) + '%';
}

// 检测碰撞
function detectCollision() {
    // 墙壁碰撞
    if (ball.x + ball.radius > canvas.width || ball.x - ball.radius < 0) {
        ball.dx *= -1;
    }
    if (ball.y - ball.radius < 0) {
        ball.dy *= -1;
    }

    // 板子碰撞
    if (
        ball.y + ball.radius > paddle.y &&
        ball.x > paddle.x &&
        ball.x < paddle.x + paddle.width
    ) {
        ball.dy = -ball.speed;
        score += 10;
        scoreElement.innerHTML = score;
    }

    // 球落地
    if (ball.y + ball.radius > canvas.height) {
        currentHealth -= healthLossPerMiss;
        updateHealthBar();
        
        if (currentHealth <= 0) {
            gameOver();
        } else {
            // 重置球的位置
            ball.x = canvas.width / 2;
            ball.y = canvas.height / 2;
            ball.dx = ball.speed * (Math.random() > 0.5 ? 1 : -1);
            ball.dy = -ball.speed;
        }
    }
}

// 游戏结束
function gameOver() {
    clearInterval(gameLoop);
    gameStarted = false;
    startButton.style.display = 'block';
    startButton.textContent = 'Play Again';
    ctx.fillStyle = '#fff';
    ctx.font = '48px Arial';
    ctx.fillText('Game Over!', canvas.width / 2 - 100, canvas.height / 2);
    ctx.font = '24px Arial';
    ctx.fillText('Final Score: ' + score, canvas.width / 2 - 60, canvas.height / 2 + 40);
}

// 移动物体
function movePaddle() {
    paddle.x += paddle.dx;
    if (autoModes === 1) {paddle.x = ball.x - paddle.width/2}

    // 防止板子超出画布
    if (paddle.x < 0) {
        paddle.x = 0;
    }
    if (paddle.x + paddle.width > canvas.width) {
        paddle.x = canvas.width - paddle.width;
    }
}

function moveBall() {
    ball.x += ball.dx;
    ball.y += ball.dy;
}

// 绘制物体
function draw() {
    // 清空画布
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // 绘制球
    ctx.beginPath();
    ctx.arc(ball.x, ball.y, ball.radius, 0, Math.PI * 2);
    ctx.fillStyle = ball.color;
    ctx.fill();
    ctx.closePath();

    // 绘制板子
    ctx.beginPath();
    ctx.rect(paddle.x, paddle.y, paddle.width, paddle.height);
    ctx.fillStyle = paddle.color;
    ctx.fill();
    ctx.closePath();
}

// 更新游戏状态
function update() {
    movePaddle();
    moveBall();
    detectCollision();
    draw();
}

// 初始绘制
draw();