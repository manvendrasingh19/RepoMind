
import {
  LayoutDashboard,
  FolderGit2,
  Network,
  Bot,
  GitPullRequest,
  BookOpen,
  Settings,
  GitBranch,
  ChevronDown,
  Sparkles,
  PanelLeftClose,
} from "lucide-react";

interface SidebarProps {
  collapsed: boolean;
  onToggle: () => void;
}

const navigation = [
  { label: "Overview", icon: LayoutDashboard, active: true },
  { label: "Repositories", icon: FolderGit2 },
  { label: "Architecture", icon: Network },
  { label: "AI Assistant", icon: Bot },
  { label: "Pull Requests", icon: GitPullRequest },
  { label: "Onboarding", icon: BookOpen },
];

export default function Sidebar({
  collapsed,
  onToggle,
}: SidebarProps) {
  return (
    <aside className={`sidebar ${collapsed ? "sidebar-collapsed" : ""}`}>
      <div className="sidebar-brand">
        <div className="brand-icon">
          <Sparkles size={21} />
        </div>

        {!collapsed && (
          <div className="brand-name">
            <strong>RepoMind</strong>
            <span>CODE INTELLIGENCE</span>
          </div>
        )}
      </div>

      <div className="workspace-selector">
        <div className="workspace-avatar">M</div>

        {!collapsed && (
          <>
            <div className="workspace-info">
              <strong>My Workspace</strong>
              <span>Personal workspace</span>
            </div>
            <ChevronDown size={15} />
          </>
        )}
      </div>

      <div className="sidebar-section">
        {!collapsed && <span className="section-label">WORKSPACE</span>}

        <nav className="sidebar-nav">
          {navigation.map((item) => {
            const Icon = item.icon;

            return (
              <button
                key={item.label}
                className={`nav-item ${item.active ? "active" : ""}`}
                title={collapsed ? item.label : undefined}
                type="button"
              >
                <Icon size={19} />
                {!collapsed && <span>{item.label}</span>}
                {!collapsed && item.label === "Repositories" && (
                  <span className="nav-count">0</span>
                )}
              </button>
            );
          })}
        </nav>
      </div>

      <div className="sidebar-bottom">
        <button className="nav-item" type="button">
          <Settings size={19} />
          {!collapsed && <span>Settings</span>}
        </button>

        <button className="nav-item" type="button">
          <GitBranch size={19} />
          {!collapsed && <span>GitHub Integration</span>}
        </button>

        <div className="sidebar-footer">
          <button
            className="collapse-button"
            type="button"
            onClick={onToggle}
            title="Toggle sidebar"
          >
            <PanelLeftClose size={18} />
            {!collapsed && <span>Collapse sidebar</span>}
          </button>
        </div>
      </div>
    </aside>
  );
}
