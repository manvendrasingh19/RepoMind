
import { useState } from "react";
import Sidebar from "../components/layout/Sidebar";
import Topbar from "../components/layout/Topbar";

interface DashboardLayoutProps {
  children: React.ReactNode;
}

export default function DashboardLayout({
  children,
}: DashboardLayoutProps) {
  const [collapsed, setCollapsed] = useState(false);

  const handleConnectRepository = () => {
    window.alert(
      "GitHub repository connection will be available after backend integration."
    );
  };

  return (
    <div className="app-shell">
      <Sidebar
        collapsed={collapsed}
        onToggle={() => setCollapsed((value) => !value)}
      />

      <main className="main-area">
        <Topbar onConnectRepository={handleConnectRepository} />
        <div className="page-container">{children}</div>
      </main>
    </div>
  );
}
