import { motion } from "framer-motion";
import { AlertTriangle, Clock, Package, TrendingDown, Users, Barcode } from "lucide-react";

const problems = [
  { icon: Clock, title: "Slow Billing", desc: "Manual billing wastes time & creates long queues" },
  { icon: Package, title: "No Stock Control", desc: "Inventory mismatches lead to lost sales" },
  { icon: TrendingDown, title: "Unknown Profit Margin", desc: "Can't track real profit per product" },
  { icon: Users, title: "Staff Dependency", desc: "Business stops when key staff is absent" },
  { icon: Barcode, title: "Barcode Not Available", desc: "Most Indian products lack barcodes" },
];

const ProblemSection = () => (
  <section className="py-16 lg:py-24 bg-background">
    <div className="container">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        className="text-center mb-12"
      >
        <span className="text-accent font-semibold text-sm uppercase tracking-wider">The Challenge</span>
        <h2 className="text-3xl lg:text-4xl font-bold mt-2 text-foreground">
          Retailers Face These Daily Problems
        </h2>
      </motion.div>
      <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6 max-w-4xl mx-auto">
        {problems.map((p, i) => (
          <motion.div
            key={p.title}
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: i * 0.1 }}
            className="bg-card rounded-xl p-6 shadow-card border border-border hover:shadow-card-hover transition-shadow"
          >
            <div className="w-10 h-10 rounded-lg bg-destructive/10 flex items-center justify-center mb-4">
              <p.icon className="h-5 w-5 text-destructive" />
            </div>
            <h3 className="font-heading font-bold text-foreground mb-1">{p.title}</h3>
            <p className="text-sm text-muted-foreground">{p.desc}</p>
          </motion.div>
        ))}
      </div>
    </div>
  </section>
);

export default ProblemSection;
