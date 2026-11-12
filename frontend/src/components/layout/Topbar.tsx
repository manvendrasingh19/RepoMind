
import {
  Search,
  Bell,
  Plus,
  Command,
  ChevronDown,
} from "lucide-react";

interface TopbarProps {
  onConnectRepository: () => void;
}

export default function Topbar({
  onConnectRepository,
}: TopbarProps) {
  return (
    <header className="topbar">
      <div className="breadcrumb">
        <span>Workspace</span>
        <span className="breadcrumb-divider">/</span>
        <strong>Overview</strong>
      </div>

      <div className="topbar-actions">
        <button className="search-button" type="button">
          <Search size={16} />
          <span>Search anything...</span>
          <kbd><Command size={11} /> K</kbd>
        </button>

        <button className="icon-button notification-button" type="button" aria-label="Notifications">
          <Bell size={19} />
          <span className="notification-dot" />
        </button>

        <div className="topbar-divider" />

        <button className="user-profile" type="button">
          <div className="user-avatar">M</div>
          <ChevronDown size={14} />
        </button>

        <button
          className="primary-button topbar-connect"
          onClick={onConnectRepository}
          type="button"
        >
          <Plus size={17} />
          Connect repository
        </button>
      </div>
    </header>
  );
}
