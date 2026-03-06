import { motion } from "framer-motion";
import { CreditCard, Package, Heart, Calculator, UserCheck, BarChart3 } from "lucide-react";

const modules = [
  { icon: CreditCard, title: "POS Billing", desc: "Lightning-fast billing with GST compliance" },
  { icon: Package, title: "Inventory Management", desc: "Real-time stock tracking & alerts" },
  { icon: Heart, title: "CRM & Loyalty", desc: "Customer management & loyalty programs" },
  { icon: Calculator, title: "Accounting", desc: "Automated bookkeeping & reports" },
  { icon: UserCheck, title: "Employee Management", desc: "Attendance, payroll & performance" },
  { icon: BarChart3, title: "Reports & Dashboard", desc: "Insights at a glance with smart analytics" },
];

const SolutionSection = () => (
  <section className="py-16 lg:py-24 bg-secondary">
    <div className="container">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        className="text-center mb-12"
      >
        <span className="text-accent font-semibold text-sm uppercase tracking-wider">The Solution</span>
        <h2 className="text-3xl lg:text-4xl font-bold mt-2 text-foreground">
          One Smart ERP For Complete Store Management
        </h2>
      </motion.div>
      <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {modules.map((m, i) => (
          <motion.div
            key={m.title}
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: i * 0.08 }}
            className="bg-card rounded-xl p-6 shadow-card border border-border hover:shadow-card-hover transition-all group"
          >
            <div className="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center mb-4 group-hover:bg-gold-gradient transition-colors">
              <m.icon className="h-6 w-6 text-primary group-hover:text-accent-foreground" />
            </div>
            <h3 className="font-heading font-bold text-foreground mb-1">{m.title}</h3>
            <p className="text-sm text-muted-foreground">{m.desc}</p>
          </motion.div>
        ))}
      </div>
    </div>
  </section>
);

export default SolutionSection;
