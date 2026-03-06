import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion";
import { motion } from "framer-motion";

const faqs = [
  { q: "Is it GST Ready?", a: "Yes! AI-Setu ERP is fully GST compliant with automatic tax calculations, GSTIN integration, and GST-ready invoicing." },
  { q: "Is Internet Required?", a: "AI-Setu ERP is cloud-based for the best experience. However, basic billing can work offline and syncs when internet is available." },
  { q: "Do I Need Barcode?", a: "No! Our AI-powered photo detection lets you bill products without barcodes — just snap a photo and the product is identified automatically." },
  { q: "Is Support Provided?", a: "Yes, we provide 24/7 customer support via phone, email, and chat. Our team is always ready to help." },
  { q: "Is Training Included?", a: "Absolutely. We provide complete setup and training for you and your staff as part of the package." },
  { q: "What About Renewal?", a: "Annual renewal is available at a competitive rate. Refer others and earn ₹1,000 per renewal incentive!" },
];

const FAQSection = () => (
  <section className="py-16 lg:py-24 bg-secondary">
    <div className="container max-w-3xl">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        className="text-center mb-12"
      >
        <span className="text-accent font-semibold text-sm uppercase tracking-wider">FAQ</span>
        <h2 className="text-3xl lg:text-4xl font-bold mt-2 text-foreground">Frequently Asked Questions</h2>
      </motion.div>
      <Accordion type="single" collapsible className="space-y-3">
        {faqs.map((f, i) => (
          <AccordionItem key={i} value={`faq-${i}`} className="bg-card border border-border rounded-xl px-6">
            <AccordionTrigger className="font-heading font-semibold text-foreground hover:no-underline">
              {f.q}
            </AccordionTrigger>
            <AccordionContent className="text-muted-foreground">{f.a}</AccordionContent>
          </AccordionItem>
        ))}
      </Accordion>
    </div>
  </section>
);

export default FAQSection;
