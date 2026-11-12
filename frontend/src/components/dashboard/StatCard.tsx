
import type { LucideIcon } from "lucide-react";
import { ArrowUpRight } from "lucide-react";

interface StatCardProps {
  title: string;
  value: string;
  description: string;
  icon: LucideIcon;
  accent: string;
}

export default function StatCard({
  title,
  value,
  description,
  icon: Icon,
  accent,
}: StatCardProps) {
  return (
    <div className="stat-card">
      <div className="stat-card-top">
        <span>{title}</span>

        <div className={`stat-icon ${accent}`}>
          <Icon size={19} />
        </div>
      </div>

      <div className="stat-value">{value}</div>

      <div className="stat-description">
        <ArrowUpRight size={14} />
        <span>{description}</span>
      </div>
    </div>
  );
}
