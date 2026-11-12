
import {
  GitBranch,
  ArrowUpRight,
  MoreHorizontal,
  FolderGit2,
} from "lucide-react";

const repositories = [
  {
    name: "TechMatch-AI",
    description: "AI-powered job matching platform",
    language: "TypeScript",
    color: "#3B82F6",
    visibility: "Private",
    updated: "Recently updated",
  },
  {
    name: "Fusion-Integrated",
    description: "Integrated campus management platform",
    language: "Python",
    color: "#A78BFA",
    visibility: "Public",
    updated: "Recently updated",
  },
  {
    name: "Face-Recognition-System",
    description: "Facial recognition entry-exit system",
    language: "Python",
    color: "#A78BFA",
    visibility: "Private",
    updated: "Recently updated",
  },
];

export default function RecentRepositories() {
  return (
    <div className="panel repository-panel">
      <div className="panel-heading">
        <div>
          <h3>Recent repositories</h3>
          <p>Your connected codebases</p>
        </div>

        <button className="text-button" type="button">
          View all <ArrowUpRight size={14} />
        </button>
      </div>

      <div className="repository-list">
        {repositories.map((repo) => (
          <div className="repository-row" key={repo.name}>
            <div className="repo-icon">
              <FolderGit2 size={20} />
            </div>

            <div className="repo-details">
              <div className="repo-title">
                <strong>{repo.name}</strong>
                <span className={`visibility ${repo.visibility.toLowerCase()}`}>
                  {repo.visibility}
                </span>
              </div>

              <p>{repo.description}</p>

              <div className="repo-meta">
                <span className="repo-language">
                  <span
                    className="language-indicator"
                    style={{ background: repo.color }}
                  />
                  {repo.language}
                </span>
                <span>{repo.updated}</span>
              </div>
            </div>

            <button
              className="icon-button repo-more"
              type="button"
              aria-label={`More options for ${repo.name}`}
            >
              <MoreHorizontal size={19} />
            </button>
          </div>
        ))}
      </div>

      <div className="repository-footer">
        <GitBranch size={15} />
        <span>Repository examples for the initial dashboard preview</span>
      </div>
    </div>
  );
}
