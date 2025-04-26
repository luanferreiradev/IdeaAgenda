import { Component, OnInit, AfterViewInit } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { TaskManagerComponent } from './task-manager/task-manager.component';

// Define interfaces para tipagem
interface Evento {
  id: number;
  titulo: string;
  descricao: string;
  data: string;
}

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, TaskManagerComponent],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
})
export class AppComponent implements OnInit, AfterViewInit {
  title = 'task-organization-system';
  logoPath = 'assets/logo.png'; // Caminho da logo
  githubStars = 0;

  ngOnInit() {
    console.log('AppComponent inicializado.');
    // Buscar estrelas ao inicializar
    this.fetchGitHubStars();
  }

  ngAfterViewInit() {
    // Configurar o autoResize após a renderização da view
    this.setupAutoResize();
  }

  // Função para buscar o número de estrelas do GitHub
  async fetchGitHubStars() {
    const url = 'https://api.github.com/repos/luanferreiradev/IdeaAgenda';
    try {
      const response = await fetch(url);
      if (!response.ok) throw new Error('Erro ao buscar dados do GitHub');
      const data = await response.json();
      this.githubStars = data.stargazers_count || 0;
      
      // Atualiza a cada 5 minutos (300000ms)
      setTimeout(() => this.fetchGitHubStars(), 300000);
    } catch (error) {
      console.error('Erro ao buscar estrelas do GitHub:', error);
      // Em caso de erro, tenta novamente após 1 minuto
      setTimeout(() => this.fetchGitHubStars(), 60000);
    }
  }

  // Configurar autoResize para o textarea
  setupAutoResize() {
    const textarea = document.getElementById('descricao') as HTMLTextAreaElement;
    if (textarea) {
      // Função para redimensionar automaticamente o textarea
      const autoResize = (el: HTMLTextAreaElement) => {
        el.style.height = 'auto';
        el.style.height = `${el.scrollHeight}px`;
      };

      // Ajusta o tamanho inicial
      autoResize(textarea);
      
      // Adicionar listener de entrada
      textarea.addEventListener('input', () => autoResize(textarea));
      
      // Modificar o setter do value para capturar alterações programáticas
      const originalSetter = Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype, 'value')?.set;
      if (originalSetter) {
        Object.defineProperty(textarea, 'value', {
          set: function(val) {
            originalSetter.call(this, val);
            autoResize(this);
          },
          get: function() {
            return textarea.value;
          }
        });
      }
    }
  }
}
