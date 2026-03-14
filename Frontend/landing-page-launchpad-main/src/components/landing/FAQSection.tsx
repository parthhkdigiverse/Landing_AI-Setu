import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion";
import { motion } from "framer-motion";
import { useEffect, useState } from "react";
import { fetchLandingPageContent } from "@/services/api";

const FAQSection = () => {

  const [faqs, setFaqs] = useState<any[]>([]);
  const [content, setContent] = useState<any>(null);
  const [livePreview, setLivePreview] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  // 1️⃣ Fetch FAQ list + landing page content
  const fetchData = async () => {

    try {

      const [resFaqs, resContent] = await Promise.all([
        fetch("http://127.0.0.1:8000/api/faqs/"),
        fetchLandingPageContent(),
      ]);

      const faqData = await resFaqs.json();

      setFaqs(faqData || []);
      setContent(resContent);

      setLoading(false);

    } catch (err) {

      console.error("Failed to load FAQ data:", err);
      setLoading(false);

    }

  };

  useEffect(() => {
    fetchData();
  }, []);

  // 2️⃣ Live Preview (Admin changes)
  useEffect(() => {

    const handler = (event: any) => {

      if (event.data) {

        setLivePreview((prev: any) => ({
          ...prev,
          ...event.data
        }));

      }

    };

    window.addEventListener("message", handler);

    return () => window.removeEventListener("message", handler);

  }, []);

  if (loading) {
    return (
      <section className="py-16 lg:py-24 bg-secondary">
        <div className="container max-w-3xl text-center text-gray-500">
          Loading FAQs...
        </div>
      </section>
    );
  }

  return (
    <section className="py-16 lg:py-24 bg-secondary">

      <div className="container max-w-3xl">

        {/* Title */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-12"
        >

          <span className="text-accent font-semibold text-sm uppercase tracking-wider">
            FAQ
          </span>

          <h2 className="text-3xl lg:text-4xl font-bold mt-2 text-foreground">
            {livePreview?.faq_title ||
             content?.faq_title ||
             "Frequently Asked Questions"}
          </h2>

        </motion.div>

        {/* FAQ Accordion */}
        <Accordion type="single" collapsible className="space-y-3">

          {faqs.map((faq, i) => (

            <AccordionItem
              key={faq.id || i}
              value={`faq-${faq.id || i}`}
              className="bg-card border border-border rounded-xl px-6"
            >

              <AccordionTrigger className="font-heading font-semibold text-foreground hover:no-underline">
                {faq.question}
              </AccordionTrigger>

              <AccordionContent className="text-muted-foreground">
                {faq.answer}
              </AccordionContent>

            </AccordionItem>

          ))}

        </Accordion>

      </div>

    </section>
  );
};

export default FAQSection;