import { motion } from "framer-motion";
import { Store, ShoppingBag, Pill, Wrench, TrendingUp } from "lucide-react";

const types = [
  { icon: Store, title: "Kirana Store" },
  { icon: ShoppingBag, title: "General Store" },
  { icon: Pill, title: "Medical Store" },
  { icon: Wrench, title: "Hardware Store" },
  { icon: TrendingUp, title: "Margin Business Retailers" },
];

const WhoIsThisFor = () => (
  <section className="py-16 lg:py-24 bg-secondary">
    <div className="container">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        className="text-center mb-12"
      >
        <span className="text-accent font-semibold text-sm uppercase tracking-wider">Perfect For</span>
        <h2 className="text-3xl lg:text-4xl font-bold mt-2 text-foreground">Who Is This For?</h2>
      </motion.div>
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-6">
        {types.map((t, i) => (
          <motion.div
            key={t.title}
            initial={{ opacity: 0, scale: 0.9 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            transition={{ delay: i * 0.08 }}
            className="bg-card rounded-xl p-6 text-center shadow-card border border-border hover:shadow-card-hover transition-shadow"
          >
            <div className="w-14 h-14 rounded-xl bg-primary/10 flex items-center justify-center mx-auto mb-3">
              <t.icon className="h-7 w-7 text-primary" />
            </div>
            <h3 className="font-heading font-semibold text-sm text-foreground">{t.title}</h3>
          </motion.div>
        ))}
      </div>
    </div>
  </section>
);

export default WhoIsThisFor;
