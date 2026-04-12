'use client';

import { CopilotProvider } from '@/context/CopilotContext';
import CopilotDock from '@/components/CopilotDock';

export default function Providers({ children }: { children: React.ReactNode }) {
  return (
    <CopilotProvider>
      {children}
      <CopilotDock />
    </CopilotProvider>
  );
}
