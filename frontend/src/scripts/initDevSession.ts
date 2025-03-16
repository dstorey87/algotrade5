import { DevPlanManager } from '../utils/DevPlanManager';

async function initializeDevSession() {
  const manager = DevPlanManager.getInstance();

  console.log('\n=== Development Session Initialized ===');
  console.log(`Current Phase: ${manager.getCurrentPhase()}`);
  console.log('\nNext Actions:');
  manager.getNextActions().forEach(action => console.log(`- ${action}`));

  const isValid = manager.validateAgainstPlan();
  if (!isValid) {
    console.error('\n⚠️ Warning: Current development state does not match development plan');
    process.exit(1);
  }

  console.log('\n✅ Development context validated successfully');
  console.log('=======================================\n');
}

if (require.main === module) {
  initializeDevSession().catch(console.error);
}
