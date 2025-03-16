import fs from 'fs';
import path from 'path';

interface DevelopmentContext {
  currentPhase: number;
  completedTasks: string[];
  nextActions: string[];
  claudeIntegrationPoints: {
    endpoint: string;
    purpose: string;
    status: 'planned' | 'in-progress' | 'completed';
  }[];
}

export class DevPlanManager {
  private static instance: DevPlanManager;
  private context: DevelopmentContext = {
    currentPhase: 1,
    completedTasks: [],
    nextActions: [],
    claudeIntegrationPoints: []
  };
  private readonly contextPath = path.join(process.cwd(), 'dev-context.json');
  private readonly planPath = path.join(process.cwd(), 'FRONTEND_DEV_PLAN.md');

  private constructor() {
    this.loadContext();
  }

  static getInstance(): DevPlanManager {
    if (!DevPlanManager.instance) {
      DevPlanManager.instance = new DevPlanManager();
    }
    return DevPlanManager.instance;
  }

  private loadContext() {
    try {
      if (fs.existsSync(this.contextPath)) {
        this.context = JSON.parse(fs.readFileSync(this.contextPath, 'utf8'));
      } else {
        this.context = {
          currentPhase: 1,
          completedTasks: [],
          nextActions: [],
          claudeIntegrationPoints: []
        };
        this.saveContext();
      }
    } catch (error) {
      console.error('Error loading development context:', error);
      throw error;
    }
  }

  private saveContext() {
    try {
      fs.writeFileSync(this.contextPath, JSON.stringify(this.context, null, 2));
    } catch (error) {
      console.error('Error saving development context:', error);
      throw error;
    }
  }

  getCurrentPhase(): number {
    return this.context.currentPhase;
  }

  getNextActions(): string[] {
    return this.context.nextActions;
  }

  markTaskCompleted(task: string) {
    if (!this.context.completedTasks.includes(task)) {
      this.context.completedTasks.push(task);
      this.saveContext();
    }
  }

  updatePhase(phase: number) {
    this.context.currentPhase = phase;
    this.saveContext();
  }

  addNextAction(action: string) {
    if (!this.context.nextActions.includes(action)) {
      this.context.nextActions.push(action);
      this.saveContext();
    }
  }

  updateClaudeIntegrationPoint(endpoint: string, purpose: string, status: 'planned' | 'in-progress' | 'completed') {
    const point = this.context.claudeIntegrationPoints.find(p => p.endpoint === endpoint);
    if (point) {
      point.status = status;
    } else {
      this.context.claudeIntegrationPoints.push({ endpoint, purpose, status });
    }
    this.saveContext();
  }

  validateAgainstPlan(): boolean {
    try {
      const planContent = fs.readFileSync(this.planPath, 'utf8');
      // Implement validation logic here
      return true;
    } catch (error) {
      console.error('Error validating against development plan:', error);
      return false;
    }
  }
}