import { Button } from '@tremor/react';
import { HelpCircle } from 'lucide-react';
import * as Tooltip from '@radix-ui/react-tooltip';

interface ConnectionToggleProps {
  isConnected: boolean;
  onToggle: () => void;
}

const ConnectionToggle = ({ isConnected, onToggle }: ConnectionToggleProps) => {
  return (
    <div className="flex items-center gap-2">
      <Button
        variant={isConnected ? "primary" : "secondary"}
        onClick={onToggle}
      >
        {isConnected ? 'Connected' : 'Disconnected'}
      </Button>
      
      <Tooltip.Provider>
        <Tooltip.Root>
          <Tooltip.Trigger asChild>
            <button className="inline-flex">
              <HelpCircle className="h-4 w-4 text-gray-500" />
            </button>
          </Tooltip.Trigger>
          <Tooltip.Portal>
            <Tooltip.Content 
              className="z-50 rounded-md bg-white px-3 py-1.5 text-sm text-gray-900 shadow-md dark:bg-gray-800 dark:text-gray-50"
              sideOffset={5}
            >
              <p>Toggle connection to trading server</p>
              <Tooltip.Arrow className="fill-current text-white dark:text-gray-800" />
            </Tooltip.Content>
          </Tooltip.Portal>
        </Tooltip.Root>
      </Tooltip.Provider>
    </div>
  );
};

export default ConnectionToggle;