import { motion } from "framer-motion";
import { Star } from "lucide-react";

const testimonials = [
  { name: "Rajesh Patel", store: "Kirana Store, Surat", text: "AI-Setu ERP transformed my billing process. The AI photo detection is a game changer — no more barcode hassles!", rating: 5 },
  { name: "Priya Sharma", store: "Medical Store, Ahmedabad", text: "Simple to use and my staff learned it in one day. GST billing is now automatic. Highly recommended!", rating: 5 },
  { name: "Amit Desai", store: "General Store, Vadodara", text: "Finally an ERP that understands Indian retail. The pricing is fair and support team is always available.", rating: 5 },
];

const TestimonialsSection = () => (
  <section className="py-16 lg:py-24 bg-background">
    <div className="container">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        className="text-center mb-12"
      >
        <span className="text-accent font-semibold text-sm uppercase tracking-wider">Testimonials</span>
        <h2 className="text-3xl lg:text-4xl font-bold mt-2 text-foreground">What Our Customers Say</h2>
      </motion.div>
      <div className="grid md:grid-cols-3 gap-6">
        {testimonials.map((t, i) => (
          <motion.div
            key={t.name}
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: i * 0.1 }}
            className="bg-card rounded-xl p-6 shadow-card border border-border"
          >
            <div className="flex gap-1 mb-3">
              {Array.from({ length: t.rating }).map((_, j) => (
                <Star key={j} className="h-4 w-4 fill-accent text-accent" />
              ))}
            </div>
            <p className="text-sm text-muted-foreground mb-4">"{t.text}"</p>
            <div>
              <p className="font-heading font-bold text-foreground text-sm">{t.name}</p>
              <p className="text-xs text-muted-foreground">{t.store}</p>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  </section>
);

export default TestimonialsSection;
