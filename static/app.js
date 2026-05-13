async function loadTasks() {
    const res = await fetch("/api/tasks");
    const tasks = await res.json();
    const list = document.getElementById("taskList");
    const count = document.getElementById("taskCount");
    count.textContent = tasks.filter(t => !t.completed).length;

    if (tasks.length === 0) {
        list.innerHTML = '<div class="empty-state">No tasks yet. Add one above! ✨</div>';
        return;
    }

    list.innerHTML = tasks.map(task => `
        <div class="task-card ${task.completed ? 'completed' : ''}">
            <div class="task-header">
                <span class="task-title">${escapeHtml(task.title)}</span>
                <span class="priority-badge priority-${task.priority}">${task.priority}</span>
            </div>
            ${task.description ? `<div class="task-desc">${escapeHtml(task.description)}</div>` : ""}
            <div class="ai-suggestion">
                <div class="ai-label">🤖 AI Suggestion</div>
                ${escapeHtml(task.ai_suggestion || "")}
            </div>
            <div class="task-actions">
                ${!task.completed ? `<button class="btn-complete" onclick="completeTask(${task.id})">✓ Done</button>` : ""}
                <button class="btn-delete" onclick="deleteTask(${task.id})">✕ Delete</button>
            </div>
        </div>
    `).join("");
}

async function addTask() {
    const title = document.getElementById("taskTitle").value.trim();
    const desc = document.getElementById("taskDesc").value.trim();
    const btn = document.getElementById("addBtn");
    const btnText = document.getElementById("btnText");

    if (!title) { alert("Please enter a task title."); return; }

    btn.disabled = true;
    btnText.textContent = "🔄 Analyzing with AI...";

    await fetch("/api/tasks", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title, description: desc })
    });

    document.getElementById("taskTitle").value = "";
    document.getElementById("taskDesc").value = "";
    btn.disabled = false;
    btnText.textContent = "✨ Add & Analyze with AI";
    loadTasks();
}

async function completeTask(id) {
    await fetch(`/api/tasks/${id}/complete`, { method: "PATCH" });
    loadTasks();
}

async function deleteTask(id) {
    await fetch(`/api/tasks/${id}`, { method: "DELETE" });
    loadTasks();
}

function escapeHtml(text) {
    const div = document.createElement("div");
    div.appendChild(document.createTextNode(text));
    return div.innerHTML;
}

document.addEventListener("DOMContentLoaded", loadTasks);