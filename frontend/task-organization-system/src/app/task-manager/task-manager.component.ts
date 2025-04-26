import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

interface Task {
  id: number;
  title: string;
}

@Component({
  selector: 'app-task-manager',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './task-manager.component.html',
  styleUrls: ['./task-manager.component.css'],
})
export class TaskManagerComponent implements OnInit {
  tasks: Task[] = [];
  task: Partial<Task> = {};

  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.fetchTasks();
  }

  fetchTasks() {
    this.http.get<Task[]>('API_ENDPOINT/tasks').subscribe({
      next: (data) => {
        this.tasks = data;
      },
      error: () => {
        // Dados de exemplo para visualização local
        this.tasks = [
          { id: 1, title: 'Reunião com equipe' },
          { id: 2, title: 'Consulta médica' },
          { id: 3, title: 'Estudar Angular' }
        ];
      }
    });
  }

  handleSubmit() {
    if (this.task.id) {
      this.http
        .put(`API_ENDPOINT/tasks/${this.task.id}`, this.task)
        .subscribe(() => this.fetchTasks());
    } else {
      this.http.post('API_ENDPOINT/tasks', this.task).subscribe(() => this.fetchTasks());
    }
    this.task = {};
  }

  editTask(task: Task) {
    this.task = { ...task };
  }

  deleteTask(id: number) {
    this.http.delete(`API_ENDPOINT/tasks/${id}`).subscribe(() => this.fetchTasks());
  }
}
