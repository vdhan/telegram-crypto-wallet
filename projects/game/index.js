const canvas = document.querySelector("canvas");
const context = canvas.getContext("2d");

// Get references to elements in the HTML
const startGameBtn = document.querySelector("#start-game-button");
const popup = document.querySelector("#popup");
const scoreEl = document.querySelector("#score");
const popupScore = document.querySelector("#popup-score");

// Set canvas dimensions
canvas.width = innerWidth;
canvas.height = innerHeight;

// Load saved score from localStorage
let totalScore = parseInt(localStorage.getItem('savedScore')) || 0;
scoreEl.innerHTML = totalScore;

// Player class definition
class Player {
	constructor(x, y, radius, color) {
		this.x = x;
		this.y = y;
		this.radius = radius;
		this.color = color;
	}

	draw() {
		context.beginPath();
		context.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
		context.fillStyle = this.color;
		context.fill();
	}
}

// Projectile class definition
class Projectile {
	constructor(x, y, radius, color, velocity) {
		this.x = x;
		this.y = y;
		this.radius = radius;
		this.color = color;
		this.velocity = velocity;
	}

	draw() {
		context.beginPath();
		context.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
		context.fillStyle = this.color;
		context.fill();
	}

	update() {
		this.draw();
		this.x += this.velocity.x;
		this.y += this.velocity.y;
	}
}

// Enemy class definition
class Enemy {
	constructor(x, y, radius, color, velocity) {
		this.x = x;
		this.y = y;
		this.radius = radius;
		this.color = color;
		this.velocity = velocity;
	}

	draw() {
		context.beginPath();
		context.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
		context.fillStyle = this.color;
		context.fill();
	}

	update() {
		this.draw();
		this.x += this.velocity.x;
		this.y += this.velocity.y;
	}
}

const player = new Player(canvas.width / 2, canvas.height / 2, 10, "white");
let projectiles = [];
let enemies = [];
let spawnEnemies;
let currentRoundScore = 0;

// Function to save score
function saveScore() {
	localStorage.setItem('savedScore', totalScore);
}

// Main animation function
function animate() {
	const animationId = requestAnimationFrame(animate);
	context.fillStyle = "rgba(0,0,0,0.1)";
	context.fillRect(0, 0, canvas.width, canvas.height);
	player.draw();

	// Update projectiles
	projectiles.forEach((projectile, pidx) => {
		projectile.update();
		if (projectile.x + projectile.radius < 0 || projectile.y + projectile.radius < 0 ||
			projectile.x - projectile.radius > canvas.width || projectile.y - projectile.radius > canvas.height) {
			projectiles.splice(pidx, 1);
		}

		// Check for collisions with enemies
		enemies.forEach((enemy, idx) => {
			const dist = Math.hypot(projectile.x - enemy.x, projectile.y - enemy.y);
			if (dist < enemy.radius + projectile.radius) {
				if (enemy.radius > 10) {
					currentRoundScore += 100;
					enemy.radius -= 10;
				} else {
					currentRoundScore += 250;
					enemies.splice(idx, 1);
				}
				projectiles.splice(pidx, 1);
				scoreEl.innerHTML = totalScore + currentRoundScore; // Update score display
			}
		});
	});

	// Update enemies and check for collisions with player
	enemies.forEach((enemy) => {
		enemy.update();
		const dist = Math.hypot(enemy.x - player.x, enemy.y - player.y);
		if (dist < enemy.radius + player.radius) {
			cancelAnimationFrame(animationId);
			clearInterval(spawnEnemies);
			// popupScore.innerHTML = totalScore + currentRoundScore;
			// popup.style.display = "flex"; // Show the popup
			askToSaveScore();
		}
	});
}

// Function to ask player whether to save or reset the score
function askToSaveScore() {
	const savePoints =  confirm('Do you want to save your score?');
	if (savePoints) {
		totalScore += currentRoundScore;
		saveScore();
	} else {
		currentRoundScore = 0; // Reset current score
	}
}

// Event listener for starting the game
startGameBtn.addEventListener("click", () => {
	popup.style.display = "none";
	projectiles = [];
	enemies = [];
	currentRoundScore = 0; // Reset score for the new round
	scoreEl.innerHTML = totalScore + currentRoundScore;

	animate();
	spawnEnemies = setInterval(() => {
		const radius = Math.random() * 15 + 10;
		let x, y;

		if (Math.random() < 0.5) {
			x = Math.random() < 0.5 ? 0 - radius : canvas.width + radius;
			y = Math.random() * canvas.height;
		} else {
			x = Math.random() * canvas.width;
			y = Math.random() < 0.5 ? 0 - radius : canvas.height + radius;
		}

		const color = `hsl(${Math.random() * 360}, 50%, 50%)`;
		const angle = Math.atan2(canvas.height / 2 - y, canvas.width / 2 - x);
		const velocity = {
			x: Math.cos(angle),
			y: Math.sin(angle),
		};
		enemies.push(new Enemy(x, y, radius, color, velocity));
	}, 1000);
});

// Add event listener to shoot projectiles
addEventListener("click", (event) => {
	const angle = Math.atan2(event.clientY - canvas.height / 2, event.clientX - canvas.width / 2);
	const velocity = {
		x: Math.cos(angle) * 5,
		y: Math.sin(angle) * 5,
	};
	projectiles.push(new Projectile(canvas.width / 2, canvas.height / 2, 5, "white", velocity));
});

// Create a restart button in HTML
const restartBtn = document.createElement("button");
restartBtn.innerText = "Restart";
restartBtn.style.position = "absolute";
restartBtn.style.top = "50%";
restartBtn.style.left = "50%";
restartBtn.style.transform = "translate(-50%, -50%)";
restartBtn.style.padding = "20px";
restartBtn.style.fontSize = "20px";
restartBtn.style.display = "none"; // Hidden initially
document.body.appendChild(restartBtn);

// Function to restart the game
function restartGame() {
	restartBtn.style.display = "none";
	projectiles = [];
	enemies = [];
	currentRoundScore = 0; // Reset current score
	scoreEl.innerHTML = totalScore + currentRoundScore;
	animate();
	spawnEnemies = setInterval(() => {
		const radius = Math.random() * 15 + 10;
		let x, y;

		if (Math.random() < 0.5) {
			x = Math.random() < 0.5 ? 0 - radius : canvas.width + radius;
			y = Math.random() * canvas.height;
		} else {
			x = Math.random() * canvas.width;
			y = Math.random() < 0.5 ? 0 - radius : canvas.height + radius;
		}

		const color = `hsl(${Math.random() * 360}, 50%, 50%)`;
		const angle = Math.atan2(canvas.height / 2 - y, canvas.width / 2 - x);
		const velocity = {
			x: Math.cos(angle),
			y: Math.sin(angle),
		};
		enemies.push(new Enemy(x, y, radius, color, velocity));
	}, 1000);
}

// Update the enemies collision with player
enemies.forEach((enemy) => {
	enemy.update();
	const dist = Math.hypot(enemy.x - player.x, enemy.y - player.y);
	if (dist < enemy.radius + player.radius) {
		// Player loses, show the restart button
		restartBtn.style.display = "block";
		clearInterval(spawnEnemies); // Stop spawning new enemies
		cancelAnimationFrame(animationId); // Stop the animation loop
	}
});

// Add event listener to restart the game
restartBtn.addEventListener("click", restartGame);

