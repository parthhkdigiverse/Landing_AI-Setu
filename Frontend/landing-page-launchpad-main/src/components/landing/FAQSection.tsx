import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion";
import { motion } from "framer-motion";
import { useEffect, useState } from "react";
import { fetchLandingPageContent, LandingPageContent } from "@/services/api";

import { FAQSkeleton } from "@/components/landing/LandingSkeleton";

const FAQSection = ({ content: propContent }: { content?: LandingPageContent | null }) => {
  const [content, setContent] = useState<LandingPageContent | null>(propContent || null);
  const [loading, setLoading] = useState(!propContent);

  // Sync state if prop changes (e.g. from live preview in parent)
  useEffect(() => {
    if (propContent) {
      setContent(propContent);
      setLoading(false);
    }
  }, [propContent]);

  // Fetch database content only if not provided as prop
  useEffect(() => {
    if (propContent) return;

    const fetchData = async () => {
      try {
        const resContent = await fetchLandingPageContent();
        if (resContent) {
          setContent(resContent);
        }
      } catch (err) {
        console.error("Failed to load FAQ data:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [propContent]);

  // 2️⃣ Live Preview (Admin changes)
  useEffect(() => {
    const handler = (event: any) => {
      if (event.data && event.data.source === 'django-admin') {
        if (event.data.model === 'LandingPageContent' || event.data.model === 'FAQContent') {
          setContent((prev: any) => ({ ...prev, ...event.data.payload }));
        } else if (event.data.model === 'FAQ') {
          const item = event.data.payload;
          const pk = event.data.pk;
          setContent((prev: any) => {
            if (!prev || !prev.faqs) return prev;
            const updatedFaqs = prev.faqs.map((f: any) => (f.id === parseInt(pk) || f.id === pk) ? { ...f, ...item } : f);
            return { ...prev, faqs: updatedFaqs };
          });
        }
      }
    };
    window.addEventListener("message", handler);
    return () => window.removeEventListener("message", handler);
  }, []);

  if (loading) {
    return (
      <section className="py-16 lg:py-24 bg-secondary">
        <FAQSkeleton />
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
            {content?.faq_label || "FAQ"}
          </span>

          <h2 className="text-3xl lg:text-4xl font-bold mt-2 text-foreground">
            {content?.faq_title || "Frequently Asked Questions"}
          </h2>

        </motion.div>

        {/* FAQ Accordion */}
        <Accordion type="single" collapsible className="space-y-3">

          {content?.faqs?.map((faq: any, i: number) => (

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