let kanbanSocket;
function initKanban(projectId) {
  kanbanSocket = io("/kanban");
  kanbanSocket.emit("join", { project_id: projectId });

  document.querySelectorAll("#board ul").forEach((list) => {
    new Sortable(list, {
      group: "kanban",
      animation: 150,
      onEnd(evt) {
        const taskId = evt.item.dataset.id;
        const status = evt.to.id;
        kanbanSocket.emit("move_task", {
          project_id: projectId,
          task_id: taskId,
          status,
        });
      },
    });
  });

  kanbanSocket.on("task_moved", (data) => {
    const el = document.querySelector(`[data-id="${data.task_id}"]`);
    if (el) {
      document.getElementById(data.status).appendChild(el);
    }
  });
}