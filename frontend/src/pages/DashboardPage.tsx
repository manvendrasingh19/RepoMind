
import {
  GitBranch,
  FileCode2,
  Network,
  Activity,
  Sparkles,
  ArrowRight,
  Clock3,
  CircleCheck,
  LoaderCircle,
} from "lucide-react";

import { lazy, Suspense } from "react";

import StatCard from "../components/dashboard/StatCard";
import RecentRepositories from "../components/dashboard/RecentRepositories";

const LanguageChart = lazy(
  () => import("../components/dashboard/LanguageChart")
);

export default function DashboardPage() {
  return (
    <div className="dashboard">
      <section className="welcome-section">
        <div>
          <div className="eyebrow">
            <Sparkles size={14} />
            YOUR DEVELOPER WORKSPACE
          </div>

          <h1>Welcome to RepoMind<span>.</span></h1>

          <p>
            Understand your codebase. Explore its architecture.
            Build with confidence.
          </p>
        </div>

        <div className="welcome-date">
          <span className="status-dot" />
          Workspace ready
        </div>
      </section>

      <section className="stats-grid">
        <StatCard
          title="Connected repositories"
          value="03"
          description="Demo repositories"
          icon={GitBranch}
          accent="blue"
        />

        <StatCard
          title="Indexed files"
          value="1,284"
          description="Illustrative count"
          icon={FileCode2}
          accent="purple"
        />

        <StatCard
          title="Code symbols"
          value="8,642"
          description="Illustrative count"
          icon={Network}
          accent="cyan"
        />

        <StatCard
          title="Analysis jobs"
          value="12"
          description="Demo activity"
          icon={Activity}
          accent="orange"
        />
      </section>

      <section className="content-grid">
        <RecentRepositories />
        <Suspense
            fallback={
                <div className="panel">
                <p>Loading language analytics...</p>
                </div>
            }
            >
            <LanguageChart />
        </Suspense>
      </section>

      <section className="bottom-grid">
        <div className="panel activity-panel">
          <div className="panel-heading">
            <div>
              <h3>Recent activity</h3>
              <p>Latest workspace events</p>
            </div>

            <button className="icon-button" type="button" aria-label="Activity options">
              <Clock3 size={18} />
            </button>
          </div>

          <div className="activity-item">
            <div className="activity-icon success">
              <CircleCheck size={17} />
            </div>

            <div>
              <strong>Workspace initialized</strong>
              <p>RepoMind environment is ready</p>
            </div>

            <span className="activity-time">Just now</span>
          </div>

          <div className="activity-item">
            <div className="activity-icon processing">
              <LoaderCircle size={17} />
            </div>

            <div>
              <strong>Repository indexing</strong>
              <p>Will be available after backend integration</p>
            </div>

            <span className="activity-time">Upcoming</span>
          </div>
        </div>

        <div className="ai-banner">
          <div className="ai-banner-icon">
            <Sparkles size={23} />
          </div>

          <span className="ai-label">INTRODUCING REPOMIND AI</span>

          <h3>Your codebase, understood.</h3>

          <p>
            Ask questions, discover dependencies, and understand
            complex code without manually exploring every file.
          </p>

          <button className="ai-button" type="button">
            Explore AI assistant
            <ArrowRight size={16} />
          </button>
        </div>
      </section>

      <footer className="dashboard-footer">
        <span>RepoMind © 2026</span>
        <span>Built for developers, by developers.</span>
      </footer>
    </div>
  );
}
