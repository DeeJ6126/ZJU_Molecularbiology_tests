#!/usr/bin/env python3
"""Translate Chinese prompts, explanations, and reference answers to English
for the molecular biology exam question bank.
Translation-type questions are preserved in Chinese.
"""

import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
INPUT_PATH = os.path.join(PROJECT_ROOT, "public", "question-bank.json")
OUTPUT_PATH = INPUT_PATH  # overwrite in-place


def build_translations():
    """Return a dict mapping question ID -> {field: translation}."""
    T = {}

    # =========================================================================
    # TRUE-FALSE (13 questions)
    # =========================================================================
    T["true-false-1-q-001"] = {
        "prompt": "Genetic codons are always universal (Genetic codons are always universal)",
        "explanation": (
            "Mitochondrial and chloroplast codons have numerous exceptions "
            "(e.g., human mitochondrial UGA encodes tryptophan rather than stop codon); "
            "some organisms also have variations in their nuclear genome codons, "
            "so the genetic code is not absolutely universal."
        ),
    }
    T["true-false-1-q-002"] = {
        "prompt": "The initiating amino acid for prokaryotic translation is fMet, and for eukaryotic translation is Met",
        "explanation": (
            "Prokaryotic initiator tRNA carries formylmethionine (fMet), "
            "while eukaryotic initiation uses unmodified methionine (Met)."
        ),
    }
    T["true-false-1-q-003"] = {
        "prompt": "Prokaryotes rely on the SD sequence to accomplish translation initiation",
        "explanation": (
            "The conserved SD (Shine-Dalgarno) sequence in the 5'UTR of prokaryotic mRNA "
            "is complementary to the 16S rRNA of the ribosome, positioning the start codon."
        ),
    }
    T["true-false-1-q-004"] = {
        "prompt": "The mRNAs of the CAP, lac, ara, and trp operons all contain SD sequences",
        "explanation": (
            "Each open reading frame (ORF) in prokaryotic polycistronic mRNA has its own "
            "independent SD sequence upstream, ensuring independent translation of each gene."
        ),
    }
    T["true-false-1-q-005"] = {
        "prompt": "All transcription processes of the Class III transcription complex require the TFIII A factor",
        "explanation": (
            "Only transcription of 5S rRNA by RNA polymerase III depends on TFIII A; "
            "other Pol III transcripts such as tRNA and U6 snRNA do not require this factor."
        ),
    }
    T["true-false-2-q-006"] = {
        "prompt": "RdDP (DNA-dependent DNA polymerase) participates in DNA replication",
        "explanation": (
            "RdDP is the core catalytic enzyme of DNA replication, responsible for "
            "synthesizing new DNA strands using DNA as a template."
        ),
    }
    T["true-false-3-q-007"] = {
        "prompt": "Eukaryotic miRNA precursors (pri-miRNA) are long RNA molecules with a stem-loop structure",
        "explanation": (
            "The stem-loop structure of pri-miRNA is an essential feature recognized and "
            "cleaved by the Drosha enzyme, and is a key intermediate in miRNA biogenesis."
        ),
    }
    T["true-false-3-q-008"] = {
        "prompt": "Enhancers are proteins that regulate genes",
        "explanation": (
            "Enhancers are cis-acting DNA sequences that exert regulatory functions by "
            "binding trans-acting factors such as transcription factors; they are not proteins themselves."
        ),
    }
    T["true-false-3-q-009"] = {
        "prompt": "The Cas13 protein family mediates RNA knockdown",
        "explanation": (
            "The CRISPR/Cas13 system specifically cleaves single-stranded RNA to achieve "
            "post-transcriptional gene silencing; it does not act on DNA."
        ),
    }
    T["true-false-3-q-010"] = {
        "prompt": "The physiological function of siRNA is to mediate post-transcriptional gene silencing",
        "explanation": (
            "siRNA guides the RISC complex to degrade target mRNA, specifically inhibiting "
            "gene expression; this is an important antiviral defense mechanism in eukaryotes."
        ),
    }
    T["true-false-4-q-011"] = {
        "prompt": "Maternal nurturing (mothering) behavior can influence the nurturing behavior of female offspring, and the trait can be transmitted across generations",
        "explanation": (
            "Classic rat epigenetics experiments have shown that maternal nurturing behavior "
            "influences the nurturing behavior of offspring in adulthood by altering the "
            "methylation pattern of the glucocorticoid receptor gene in the offspring's hippocampus, "
            "and this trait can be transmitted across generations."
        ),
    }
    T["true-false-5-q-012"] = {
        "prompt": "The Agrobacterium helper plasmid carries vir virulence genes",
        "explanation": (
            "In the Agrobacterium binary vector system, the helper plasmid retains the vir "
            "virulence region, encoding the proteins required for T-DNA transfer, while T-DNA "
            "is located on a separate mini-Ti plasmid."
        ),
    }
    T["true-false-5-q-013"] = {
        "prompt": "In blue-white screening, colonies with the exogenous target fragment inserted into the vector appear white",
        "explanation": (
            "When an exogenous fragment is inserted into the lacZα gene of the vector, "
            "it disrupts the activity of the encoded β-galactosidase α-subunit, "
            "preventing the cleavage of the substrate X-gal to produce a blue color; "
            "therefore, colonies appear white. Vectors without an insert express the "
            "intact α-subunit, and colonies appear blue."
        ),
    }

    # =========================================================================
    # MULTIPLE-CHOICE (17 questions)
    # =========================================================================
    T["multiple-choice-1-q-001"] = {
        "prompt": "Who invented PCR technology?",
        "explanation": (
            "In 1983, Kary Mullis invented the polymerase chain reaction (PCR) technique, "
            "which revolutionized molecular biology research."
        ),
    }
    T["multiple-choice-1-q-002"] = {
        "prompt": "In the experiment demonstrating that DNA is the genetic material, which radioisotope was used to label proteins?",
        "explanation": (
            "Proteins contain sulfur but not phosphorus, while DNA contains phosphorus but "
            "not sulfur. Therefore, the Hershey-Chase experiment used ³⁵S to label "
            "proteins and ³²P to label DNA."
        ),
    }
    T["multiple-choice-2-q-003"] = {
        "prompt": "What is the first amino acid in prokaryotic translation initiation?",
        "explanation": (
            "Prokaryotic initiator tRNA carries formylmethionine (fMet), while eukaryotic "
            "initiator tRNA carries unmodified methionine."
        ),
    }
    T["multiple-choice-2-q-004"] = {
        "prompt": "What amino acid is encoded by the AUG codon?",
        "explanation": (
            "AUG is both the start codon and the codon for methionine. In prokaryotes, "
            "it encodes fMet at the initiation position and Met during elongation; in "
            "eukaryotes, it encodes Met in both contexts."
        ),
    }
    T["multiple-choice-2-q-005"] = {
        "prompt": "In which type of organism is the SD sequence exclusively found in mRNA?",
        "explanation": (
            "The SD sequence is a ribosome-binding site unique to prokaryotic mRNA. "
            "Eukaryotic mRNA relies on the 5' cap structure and Kozak sequence to recruit ribosomes."
        ),
    }
    T["multiple-choice-2-q-006"] = {
        "prompt": "In prokaryotic translation, which elongation factor transports aminoacyl-tRNA to the ribosomal A site?",
        "explanation": (
            "The EF-Tu-GTP complex binds aminoacyl-tRNA and transports it to the ribosomal A site; "
            "EF-G is responsible for translocating the ribosome along the mRNA."
        ),
    }
    T["multiple-choice-2-q-007"] = {
        "prompt": "What is the definition of the Wobble theory (Wobble hypothesis)?",
        "explanation": (
            "The wobble hypothesis explains the degeneracy of the genetic code, "
            "reducing the number of tRNA species required by the cell."
        ),
    }
    T["multiple-choice-3-q-008"] = {
        "prompt": "What is the core function of the CRISPR/Cas13 system?",
        "explanation": (
            "Cas13 is an RNA-targeting CRISPR effector protein that specifically cleaves "
            "single-stranded RNA and is used for post-transcriptional regulation of gene expression."
        ),
    }
    T["multiple-choice-3-q-009"] = {
        "prompt": "What is the key enzyme for processing pre-miRNA into mature miRNA?",
        "explanation": (
            "After pre-miRNA is transported to the cytoplasm by Exportin-5, "
            "it is cleaved by the Dicer enzyme to produce a mature miRNA duplex of approximately 22 nt."
        ),
    }
    T["multiple-choice-3-q-010"] = {
        "prompt": "What is the alternative name for the coding strand?",
        "explanation": (
            "The coding strand has the same sequence as the transcribed mRNA "
            "(except for T/U replacement), and is therefore also called the sense strand "
            "or non-template strand."
        ),
    }
    T["multiple-choice-3-q-011"] = {
        "prompt": "What components make up the transcription ternary complex?",
        "explanation": (
            "The sigma factor only participates in transcription initiation and dissociates "
            "during the elongation phase; therefore, it is not part of the ternary complex."
        ),
    }
    T["multiple-choice-3-q-012"] = {
        "prompt": "Why does transcription of long mRNAs take a very long time?",
        "explanation": (
            "RNA polymerase frequently undergoes abortive transcription during the initiation "
            "phase (synthesizing short RNA fragments before dissociating). Long genes require "
            "multiple successful initiation events to complete full-length transcription, "
            "thus taking longer overall."
        ),
    }
    T["multiple-choice-3-q-013"] = {
        "prompt": "What elements are essential for pre-mRNA splicing?",
        "explanation": (
            "5' capping and 3' polyadenylation are independent post-transcriptional "
            "modifications and are not part of the splicing process. Splicing requires "
            "recognition of three core elements: the 5' GU, the 3' AG, and the branch point adenosine."
        ),
    }
    T["multiple-choice-4-q-014"] = {
        "prompt": "What key gene does the helper vector of the Agrobacterium binary vector system carry?",
        "explanation": (
            "The vir (virulence) genes encode a series of proteins required for T-DNA transfer "
            "and are key to Agrobacterium-mediated plant genetic transformation."
        ),
    }
    T["multiple-choice-5-q-015"] = {
        "prompt": "What two core domains do transcription factors generally contain?",
        "explanation": (
            "These two domains are the basis of transcription factor function; "
            "the yeast two-hybrid system exploits this property."
        ),
    }
    T["multiple-choice-5-q-016"] = {
        "prompt": "Which of the following operations cannot improve the solubility of bacterially expressed recombinant proteins?",
        "explanation": (
            "Simultaneously expressing multiple proteins competes for intracellular chaperones "
            "and folding machinery, leading to more proteins forming inclusion bodies. Lowering "
            "temperature, using fusion tags (such as MBP), and co-expressing molecular chaperones "
            "can improve protein solubility."
        ),
    }
    T["multiple-choice-5-q-017"] = {
        "prompt": "Given a known upstream primer and one template strand in PCR, what is the rule for selecting the downstream primer?",
        "explanation": (
            "PCR amplification requires a pair of primers that respectively bind the two "
            "template strands in opposite orientations to amplify the target fragment between them."
        ),
    }

    # =========================================================================
    # SHORT-ANSWER (61 questions)
    # =========================================================================
    T["short-answer-1-q-001"] = {
        "prompt": "Assembly process of the eukaryotic Class II transcription preinitiation complex (PIC)",
        "referenceAnswer": (
            "① TFIID (containing TBP and TAFs) first binds to the TATA box of the promoter, forming the initial binding core;\n"
            "② TFIIA and TFIIB bind sequentially, stabilizing the TFIID-DNA interaction;\n"
            "③ TFIIF binds to RNA polymerase II (Pol II), guiding Pol II into the promoter region;\n"
            "④ TFIIE and TFIIH are sequentially recruited, forming the complete transcription preinitiation complex;\n"
            "⑤ The helicase activity of TFIIH unwinds the DNA duplex to form a transcription bubble, while its kinase activity phosphorylates the C-terminal domain (CTD) of Pol II, triggering the transition to transcription elongation."
        ),
    }
    T["short-answer-1-q-002"] = {
        "prompt": "What RNA polymerases exist besides Pol I-III? What are their respective functions?",
        "referenceAnswer": (
            "① Plant-specific Pol IV: located in chromatin, transcribes siRNA precursors, participates in the RNA-directed DNA methylation (RdDM) pathway, mediating transposon silencing and gene expression regulation;\n"
            "② Plant-specific Pol V: transcribes non-coding RNAs that serve as scaffolds to recruit siRNA-Ago4 complexes, directing DNA methylation and heterochromatin formation;\n"
            "③ Mitochondrial RNA polymerase: a single-subunit enzyme that transcribes all genes of the mitochondrial genome;\n"
            "④ Chloroplast RNA polymerase: includes nuclear-encoded RNA polymerase (NEP) and chloroplast-encoded RNA polymerase (PEP), which together transcribe the chloroplast genome;\n"
            "⑤ Bacteriophage RNA polymerases: such as T7, SP6, and T3 phage RNA polymerases, which specifically recognize their own promoters and efficiently transcribe downstream sequences; widely used in in vitro transcription experiments."
        ),
    }
    T["short-answer-1-q-003"] = {
        "prompt": "Two mechanisms of transcription termination (prokaryotes)",
        "referenceAnswer": (
            "① Rho-independent termination: the 3' end of the transcript forms a GC-rich hairpin structure, followed by a stretch of U residues; rU-dA base pairs are poorly stable, causing RNA polymerase to dissociate from the template strand;\n"
            "② Rho-dependent termination: the Rho factor binds to the rut site on the transcript, uses the energy of ATP hydrolysis to move along the RNA toward the 3' end, catches up with RNA polymerase, and dissociates it from the DNA template, terminating transcription."
        ),
    }
    T["short-answer-1-q-004"] = {
        "prompt": "Four core functions of the CTD domain of RNA Pol II",
        "referenceAnswer": (
            "① Transcription initiation regulation: the phosphorylation state of the CTD determines the transition from transcription initiation to elongation;\n"
            "② Recruitment of capping enzyme: in early transcription, phosphorylated CTD recruits the capping complex to complete mRNA 5' capping;\n"
            "③ Regulation of splicing: CTD recruits splicing factors, coordinating the coupling of transcription and pre-mRNA splicing;\n"
            "④ Recruitment of polyadenylation complex: in late transcription, CTD recruits the polyadenylation complex to complete mRNA 3' polyadenylation."
        ),
    }
    T["short-answer-1-q-005"] = {
        "prompt": "Definition and types of cis-acting elements",
        "referenceAnswer": (
            "Definition: DNA sequences located on the same chromosome as the gene they regulate; they do not encode proteins themselves, but regulate gene expression by binding trans-acting factors;\n\n"
            "Types: ① Promoter: located upstream of the gene transcription start site, the core region where RNA polymerase binds; "
            "② Enhancer: can enhance transcription activity from upstream, downstream, within, or even at a distance from the gene, independent of position and orientation; "
            "③ Silencer: inhibits gene transcription, also independent of position and orientation; "
            "④ Insulator: blocks the regulatory effects of enhancers or silencers on adjacent genes, maintaining the independence of gene expression."
        ),
    }
    T["short-answer-2-q-006"] = {
        "prompt": "Key differences between prokaryotic and eukaryotic translation initiation",
        "referenceAnswer": (
            "Assembly of the prokaryotic 30S translation initiation complex:\n"
            "① After translation termination, IF1 binds to the ribosome, promoting dissociation of the large and small subunits;\n"
            "② IF3 binds to the 30S small subunit, preventing its re-association with the 50S large subunit;\n"
            "③ IF1 and IF2-GTP bind to the 30S small subunit;\n"
            "④ mRNA binds via complementary pairing between the SD sequence and the 16S rRNA of the 30S small subunit, a process mediated by IF3;\n"
            "⑤ fMet-tRNAfMet enters the P site and pairs with the AUG start codon;\n"
            "⑥ GTP is hydrolyzed, and IF1, IF2, and IF3 are released;\n"
            "⑦ The 50S large subunit associates with the 30S small subunit, forming the complete 70S initiation complex."
        ),
    }
    T["short-answer-2-q-007"] = {
        "prompt": "Assembly process of the eukaryotic 80S translation initiation complex",
        "referenceAnswer": (
            "① The 40S small subunit binds eIF-3 to form the 40SN complex;\n"
            "② Met-tRNAiMet and eIF2-GTP bind to 40SN, forming the 43S preinitiation complex;\n"
            "③ With the assistance of the eIF4F complex (containing eIF4E, eIF4G, and eIF4A), the 43S complex binds to the 5' cap structure of mRNA, forming the 48S initiation complex;\n"
            "④ The initiation complex scans along the mRNA in the 5'→3' direction to locate the AUG start codon;\n"
            "⑤ With the assistance of eIF5 and eIF5B, the 60S large subunit associates with the 40S small subunit;\n"
            "⑥ GTP is hydrolyzed, all initiation factors are released, and the complete 80S initiation complex is formed."
        ),
    }
    T["short-answer-2-q-008"] = {
        "prompt": "What types of RNA are required in the translation process? Describe their biological functions",
        "referenceAnswer": (
            "① mRNA (messenger RNA): carries the coding information of genes, serves as the template for translation; its codon sequence determines the amino acid sequence of the protein;\n"
            "② tRNA (transfer RNA): serves as the carrier of amino acids; each tRNA specifically recognizes and binds one amino acid, and through complementary base pairing between its anticodon and the codon on mRNA, accurately delivers amino acids to the corresponding position on the ribosome;\n"
            "③ rRNA (ribosomal RNA): together with proteins, constitutes the large and small subunits of the ribosome and is the structural core of the ribosome; the 23S/28S rRNA of the large subunit possesses peptidyl transferase activity, catalyzing peptide bond formation and ensuring the smooth progression of translation."
        ),
    }
    T["short-answer-2-q-009"] = {
        "prompt": "Three tRNA-binding sites on the ribosome and their functions",
        "referenceAnswer": (
            "① A site (aminoacyl site): the position where aminoacyl-tRNA enters the ribosome; new amino acids are added to the elongating peptide chain here;\n"
            "② P site (peptidyl site): the position where the peptidyl-tRNA carrying the growing peptide chain binds;\n"
            "③ E site (exit site): the position where deacylated tRNA (having unloaded its amino acid) temporarily binds before dissociating from the ribosome."
        ),
    }
    T["short-answer-2-q-010"] = {
        "prompt": "Elongation factors required during translation elongation and their functions",
        "referenceAnswer": (
            "① EF-Tu: binds GTP to form the EF-Tu-GTP complex, escorting aminoacyl-tRNA into the ribosomal A site;\n"
            "② EF-Ts: catalyzes the exchange of GDP for GTP, regenerating EF-Tu-GTP from EF-Tu-GDP so that it can be recycled;\n"
            "③ EF-G: after binding GTP, enters the ribosomal A site and uses the energy of GTP hydrolysis to drive the ribosome to move one codon along the mRNA, translocating peptidyl-tRNA from the A site to the P site and deacylated tRNA from the P site to the E site."
        ),
    }
    T["short-answer-2-q-011"] = {
        "prompt": "Translation initiation principles of the SD sequence, Kozak sequence, and IRES",
        "referenceAnswer": (
            "① SD sequence: a conserved sequence (AGGAGGU) in the 5'UTR of prokaryotic mRNA, located approximately 10 nt upstream of the start codon; it is complementary to the 3' end of the 16S rRNA of the 30S small subunit, directly positioning the ribosome at the start codon;\n"
            "② Kozak sequence: a conserved sequence (GCCRCC AUG G) surrounding the AUG start codon in eukaryotic mRNA, which enhances the efficiency of start codon recognition by the ribosome and improves the accuracy of translation initiation;\n"
            "③ IRES (Internal Ribosome Entry Site): a secondary structure element within mRNA that does not depend on the 5' cap structure or the scanning process; it directly recruits the small ribosomal subunit and assembles the initiation complex; commonly found in viral mRNA and in eukaryotic translation under stress conditions."
        ),
    }
    T["short-answer-2-q-012"] = {
        "prompt": "Three post-translational modification modes that alter protein activity",
        "referenceAnswer": (
            "① Phosphorylation: catalyzed by protein kinases, the γ-phosphate group of ATP is transferred to serine, threonine, or tyrosine residues of a protein; by altering protein conformation, it activates or inhibits enzymatic activity and is the most common regulatory mechanism in cell signal transduction; it is reversible, with phosphate groups removed by phosphatases;\n"
            "② Acetylation: catalyzed by acetyltransferases (HATs), an acetyl group is transferred to the amino group of lysine residues; this neutralizes the positive charge of lysine, altering the protein's interaction with DNA, RNA, or other proteins; a classic example is histone acetylation, which loosens chromatin and promotes gene transcription; it is reversible, with acetyl groups removed by deacetylases (HDACs);\n"
            "③ Ubiquitination: catalyzed by an enzyme cascade consisting of E1 activating enzyme, E2 conjugating enzyme, and E3 ligase, ubiquitin molecules are covalently attached to lysine residues of a protein; monoubiquitination can alter protein localization or interactions; polyubiquitination (K48-linked) marks proteins for degradation by the 26S proteasome, serving as the major pathway for selective protein degradation in cells."
        ),
    }
    T["short-answer-3-q-013"] = {
        "prompt": "Three main types of DNA replication",
        "referenceAnswer": (
            "① Theta (θ) replication: the primary replication mode of prokaryotic circular chromosomes, initiating from a single origin of replication and proceeding bidirectionally, forming a θ-shaped replication intermediate;\n"
            "② Rolling circle replication: the replication mode of phages, plasmids, and certain viruses; a nick is introduced in one strand of circular DNA, and using the intact strand as a template, new strands are synthesized in a rolling direction, producing multiple tandem genomic copies;\n"
            "③ D-loop replication: the replication mode of animal mitochondrial DNA; the replication origins of the two strands are not synchronized; first, a new strand is synthesized using one strand as a template, displacing the other strand to form a D-loop structure; when the replication fork reaches the origin of the other strand, replication using the displaced strand as a template begins."
        ),
    }
    T["short-answer-3-q-014"] = {
        "prompt": "Enzymes required for DNA replication and their functions",
        "referenceAnswer": (
            "① Helicase: uses the energy of ATP hydrolysis to unwind the DNA duplex, forming the replication fork;\n"
            "② Single-strand DNA-binding protein (SSB): binds to unwound single-stranded DNA, preventing re-annealing and degradation by nucleases;\n"
            "③ Topoisomerase: relieves the superhelical tension generated during DNA unwinding; Topoisomerase I creates single-strand nicks, Topoisomerase II creates double-strand breaks, and DNA gyrase (unique to prokaryotes) introduces negative supercoils;\n"
            "④ Primase: synthesizes RNA primers, providing a 3'-OH end for DNA polymerase;\n"
            "⑤ DNA polymerase:"
        ),
    }
    T["short-answer-3-q-015"] = {
        "prompt": "DNA Pol III (prokaryotic): the main replicative polymerase, responsible for synthesizing both the leading and lagging strands;",
        "referenceAnswer": "DNA Pol I (prokaryotic): removes RNA primers and fills in the resulting gaps;"
    }
    T["short-answer-3-q-016"] = {
        "prompt": "DNA Pol δ and ε (eukaryotic): responsible for synthesizing the lagging strand and leading strand, respectively;",
        "referenceAnswer": (
            "⑥ DNA ligase: joins Okazaki fragments on the lagging strand to form a complete DNA strand;\n"
            "⑦ Telomerase: unique to eukaryotes, uses its own RNA as a template to synthesize telomeric DNA, solving the end-replication problem of linear chromosomes."
        ),
    }
    T["short-answer-3-q-017"] = {
        "prompt": "Composition of the nucleosome",
        "referenceAnswer": (
            "The nucleosome is the basic structural unit of chromatin, consisting of a core particle and linker DNA:\n"
            "① Core particle: composed of 145-147 bp of DNA wrapped approximately 1.75 turns around a histone octamer; the histone octamer consists of two H2A-H2B dimers and one H3-H4 tetramer;\n"
            "② Linker DNA: approximately 20-60 bp in length, connecting adjacent core particles;\n"
            "③ Histone H1: binds at the entry and exit points of linker DNA on the core particle, stabilizing the nucleosome structure and facilitating the organization of nucleosomes into more compact chromatin fibers."
        ),
    }
    T["short-answer-3-q-018"] = {
        "prompt": "Three core functions of the centromere",
        "referenceAnswer": (
            "① The physical connection point for sister chromatids during cell division, ensuring that sister chromatids remain together before separation;\n"
            "② The assembly platform for the kinetochore, a protein complex that binds spindle fibers;\n"
            "③ Binding spindle microtubules, mediating chromosome movement during cell division and ensuring accurate, equal distribution of chromosomes to the two daughter cells."
        ),
    }
    T["short-answer-3-q-019"] = {
        "prompt": "Three characteristics of the centromere",
        "referenceAnswer": (
            "① Contains a large amount of highly repetitive DNA sequences, which are highly variable among species;\n"
            "② Contains a specific histone H3 variant (such as CENP-A) that replaces conventional histone H3 and is a hallmark feature of the centromere;\n"
            "③ At the centromeric region, a kinetochore structure forms on each chromatid, responsible for connecting to spindle microtubules."
        ),
    }
    T["short-answer-4-q-020"] = {
        "prompt": "Complete process of eukaryotic pre-mRNA splicing (including spliceosome assembly)",
        "referenceAnswer": (
            "① Spliceosome recognition: U1 snRNP binds to the 5' splice site (GU) of the intron, and U2 snRNP binds to the branch point adenosine sequence;\n"
            "② Spliceosome assembly: the U4/U6/U5 tri-snRNP binds to the complex, forming the complete spliceosome;\n"
            "③ First transesterification reaction: U1 and U4 snRNPs leave the spliceosome; the 2'-hydroxyl group of the branch point adenosine attacks the phosphodiester bond at the 5' splice site, cleaving the 5' exon and forming a lariat structure with the intron;\n"
            "④ Second transesterification reaction: the 3'-hydroxyl group of the 5' exon attacks the phosphodiester bond at the 3' splice site, cleaving the 3' exon and covalently joining the two adjacent exons;\n"
            "⑤ Spliceosome disassembly: the lariat intron is released and degraded, and the spliceosome components dissociate, releasing the mature mRNA."
        ),
    }
    T["short-answer-4-q-021"] = {
        "prompt": "Process and functions of mRNA 5' capping",
        "referenceAnswer": (
            "Process: ① RNA triphosphatase removes the γ-phosphate from the 5' terminal nucleotide of the precursor mRNA; "
            "② Guanylyltransferase transfers the GMP moiety of GTP to the 5' end of the mRNA via a 5'-5' triphosphate linkage; "
            "③ Methyltransferase methylates the N7 position of the guanine residue, forming a type 0 cap; "
            "④ In some mRNAs, the 2'-OH of the ribose of the first or second nucleotide is also methylated, forming type 1 or type 2 caps.\n\n"
            "Functions: ① Protects mRNA from degradation by 5' exonucleases, increasing its stability; "
            "② Facilitates mRNA transport from the nucleus to the cytoplasm; "
            "③ Enhances mRNA translation efficiency and serves as an important signal for ribosome recognition of mRNA; "
            "④ Participates in proper pre-mRNA splicing."
        ),
    }
    T["short-answer-4-q-022"] = {
        "prompt": "Process and functions of mRNA 3' polyadenylation",
        "referenceAnswer": (
            "Process: ① When transcription proceeds past the polyadenylation signal sequence (AAUAAA), an endonuclease cleaves the pre-mRNA 10-30 nt downstream of the signal sequence; "
            "② Poly(A) polymerase (PAP) uses ATP as a substrate to sequentially add approximately 200 adenylate residues to the 3' end of the mRNA, forming the poly(A) tail; "
            "③ Poly(A)-binding protein (PABP) binds to the poly(A) tail, stabilizing its structure.\n\n"
            "Functions: ① Protects mRNA from degradation by 3' exonucleases, extending its half-life; "
            "② Enhances mRNA translation efficiency; PABP interacts with eIF4G to circularize the mRNA, enhancing ribosome recruitment; "
            "③ Participates in the nuclear export of mRNA."
        ),
    }
    T["short-answer-4-q-023"] = {
        "prompt": "Process of trans-splicing",
        "referenceAnswer": (
            "Trans-splicing is a splicing mode that joins exons from two different pre-mRNA molecules, commonly found in lower eukaryotes and certain specific genes of higher organisms:\n"
            "① The branch point adenosine within the half-intron attacks the 5' splice site between the leader exon and its half-intron, forming a Y-shaped intron-exon intermediate;\n"
            "② The free 3'-hydroxyl group of the leader exon attacks the 3' splice site between the coding exon and its half-intron;\n"
            "③ The leader exon and the coding exon are covalently joined to form mature mRNA;\n"
            "④ The Y-shaped intron is released and degraded."
        ),
    }
    T["short-answer-4-q-024"] = {
        "prompt": "The complete miRNA biogenesis pathway",
        "referenceAnswer": (
            "① In the nucleus, RNA polymerase II transcribes miRNA genes to produce primary miRNA (pri-miRNA) with a stem-loop structure;\n"
            "② The Drosha-DGCR8 complex cleaves the base of the pri-miRNA stem-loop, releasing a precursor miRNA (pre-miRNA) of approximately 70 nt;\n"
            "③ The Exportin-5-RanGTP complex transports pre-miRNA to the cytoplasm;\n"
            "④ The Dicer enzyme cleaves the terminal loop of pre-miRNA, producing an miRNA duplex (miRNA/miRNA*) of approximately 22 nt;\n"
            "⑤ The duplex unwinds, and the guide strand (mature miRNA) enters the RNA-induced silencing complex (RISC), while the passenger strand (miRNA*) is typically degraded;\n"
            "⑥ The mature miRNA guides the RISC complex to target the 3'UTR of mRNA, inhibiting translation through incomplete complementarity or degrading mRNA through complete complementarity."
        ),
    }
    T["short-answer-4-q-025"] = {
        "prompt": "Detailed differences between siRNA and miRNA",
        "referenceAnswer": (
            "mRNA degradation pathways in eukaryotes:\n"
            "① 3'→5' degradation pathway: first, deadenylases remove the 3' poly(A) tail of mRNA, then the exosome complex progressively degrades the mRNA from the 3' end toward the 5' end;\n"
            "② 5'→3' degradation pathway: after deadenylation, decapping enzymes remove the 5' cap structure, then Xrn1 exonuclease degrades the mRNA from the 5' end toward the 3' end;\n"
            "③ Endonuclease-mediated degradation: specific endonucleases cleave within the mRNA, and the resulting fragments are degraded by 5'→3' and 3'→5' exonucleases, respectively;\n"
            "④ miRNA-mediated degradation: miRNA guides the RISC complex to bind target mRNA, promoting mRNA degradation through deadenylation, decapping, or direct cleavage."
        ),
    }
    T["short-answer-5-q-026"] = {
        "prompt": "What is epigenetic inheritance? List three or more examples of epigenetic phenomena",
        "referenceAnswer": (
            "Definition: Heritable changes in gene expression or cellular phenotype that occur without altering the DNA nucleotide sequence; "
            "these changes can be transmitted to daughter cells through cell division, and in some cases can be transmitted across generations to the offspring of an individual."
        ),
    }
    T["short-answer-5-q-027"] = {
        "prompt": "Epigenetic mechanisms: DNA methylation, histone modification, chromatin remodeling, non-coding RNA regulation, etc.",
        "referenceAnswer": (
            "Examples: ① X-chromosome inactivation: in early embryonic development of female mammals, one of the two X chromosomes is randomly and permanently inactivated, forming a Barr body; "
            "the inactivated X chromosome is silenced by epigenetic modifications such as DNA methylation and histone deacetylation, resolving the problem of X-chromosome gene dosage imbalance between males and females; "
            "② Genomic imprinting: the expression of certain genes depends on their parental origin, meaning that only one of the paternal and maternal alleles is expressed while the other is silenced by epigenetic modifications; "
            "for example, the insulin-like growth factor 2 (IGF2) gene is expressed only from the paternal allele, while the maternal allele is silenced by methylation; "
            "③ Transgenerational transmission of maternal behavior: maternal nurturing behavior in rats (such as licking and nursing) influences the stress response and maternal behavior of offspring in adulthood by altering the methylation pattern of the glucocorticoid receptor gene in the offspring's hippocampus, and this trait can be passed to subsequent generations; "
            "④ Stem cell differentiation: stem cells and differentiated cells have identical DNA sequences, but maintain different gene expression profiles through different epigenetic modification patterns, determining the direction of cell differentiation and function; "
            "⑤ Environmentally induced epigenetic changes: environmental factors such as nutrition, chemicals, and stress can alter an individual's epigenome, affecting gene expression and disease susceptibility, and some changes can be transmitted across generations."
        ),
    }
    T["short-answer-5-q-028"] = {
        "prompt": "Main factors/mechanisms leading to epigenetic regulation",
        "referenceAnswer": (
            "① DNA methylation: primarily occurs at the 5' position of cytosine in CpG dinucleotides, catalyzed by DNA methyltransferases (DNMTs); generally associated with gene silencing, especially hypermethylation of promoter regions, which inhibits gene transcription;\n"
            "② Histone modification: the N-terminal tails of histones can undergo various covalent modifications, including acetylation, methylation, phosphorylation, and ubiquitination; different combinations of modifications form a 'histone code' that regulates gene expression by altering chromatin compaction or recruiting other regulatory proteins; for example, H3K9 acetylation is associated with gene activation, while H3K27 trimethylation is associated with gene silencing;\n"
            "③ Non-coding RNA regulation: non-coding RNAs such as miRNA, siRNA, and lncRNA participate in epigenetic regulation through various mechanisms, including mediating DNA methylation, histone modification, and chromatin remodeling;\n"
            "④ Chromatin remodeling: chromatin remodeling complexes use the energy of ATP hydrolysis to alter the position or composition of nucleosomes, regulating DNA accessibility and thereby controlling gene expression."
        ),
    }
    T["short-answer-5-q-029"] = {
        "prompt": "Process and regulatory mechanism of m5CpG generation from CpG methylation",
        "referenceAnswer": (
            "① Actively transcribed promoters typically carry the H3K4me3 activation mark; when the ADD domain of DNMT3A/B binds H3K4me3, its methyltransferase (MTase) activity is inhibited, thus maintaining a hypomethylated state in promoter regions;\n"
            "② When chromatin state changes and the H3K4me3 modification is lost, the ADD domain of DNMT3 binds the unmodified histone N-terminal tail, relieving the inhibition of the MTase domain;\n"
            "③ DNMT3, acting as a methylation 'writer', catalyzes the methylation of the 5' position of cytosine in CpG dinucleotides, generating 5-methylcytosine (m5CpG); simultaneously, DNMT3 also acts as a 'reader', recognizing existing m5CpG modifications and promoting the methylation of adjacent CpG sites, maintaining the stability of the methylation pattern;\n"
            "④ Methylated DNA recruits methyl-CpG-binding domain proteins (MBDs), which further recruit repressive complexes such as histone deacetylases and histone methyltransferases, leading to chromatin compaction and permanent silencing of gene transcription."
        ),
    }
    T["short-answer-6-q-030"] = {
        "prompt": "List all techniques for detecting protein-protein interactions (9 methods)",
        "referenceAnswer": (
            "① Yeast two-hybrid (Y2H): based on the split activation principle of transcription factors, detects protein-protein interactions in living cells and can be used to screen for unknown interacting proteins;\n"
            "② Co-immunoprecipitation (Co-IP): uses a specific antibody against a target protein to capture the target protein and its bound protein complexes from cell lysates, followed by Western blot identification of interacting proteins;\n"
            "③ GST Pull-down: the target protein is expressed as a fusion with a GST tag and immobilized on glutathione affinity resin, capturing interacting proteins from cell lysates; suitable for in vitro validation of protein interactions;\n"
            "④ Far Western blotting: proteins separated by electrophoresis are transferred to a membrane and probed with a labeled bait protein to detect interacting target proteins on the membrane, directly revealing the molecular weight of interacting proteins;\n"
            "⑤ Fluorescence resonance energy transfer (FRET): uses the energy transfer phenomenon between two fluorophores to detect close-range protein-protein interactions (<10 nm) in real time in living cells;\n"
            "⑥ Bimolecular fluorescence complementation (BiFC): a fluorescent protein is split into two inactive fragments, each fused to one of the two test proteins; if the two proteins interact, the fluorescent protein fragments reassemble into an active fluorescent protein, producing a fluorescent signal;\n"
            "⑦ Protein microarray technology: large numbers of proteins are immobilized on a chip, and labeled bait protein is used to screen for interacting proteins, enabling high-throughput detection of protein interactions;\n"
            "⑧ Surface plasmon resonance (SPR): detects changes in surface plasmon resonance signals caused by biomolecular binding, enabling real-time, quantitative analysis of the kinetic parameters of protein-protein interactions;\n"
            "⑨ Affinity purification-mass spectrometry (AP-MS): the target protein and its complexes are purified using a tag (such as Flag or HA), and all protein components of the complex are identified by mass spectrometry, enabling systematic analysis of protein interaction networks."
        ),
    }
    T["short-answer-6-q-031"] = {
        "prompt": "Three main techniques for detecting DNA-protein interactions",
        "referenceAnswer": (
            "① Electrophoretic mobility shift assay (EMSA): an in vitro assay in which a labeled DNA probe is incubated with the test protein and separated by non-denaturing polyacrylamide gel electrophoresis; when protein binds to DNA, the electrophoretic mobility of the complex is retarded, producing a 'shifted' band, allowing qualitative detection of protein-DNA binding;\n"
            "② Chromatin immunoprecipitation (ChIP): an in vivo assay in which protein and DNA are crosslinked with formaldehyde in living cells, chromatin is fragmented by sonication, and the target protein-DNA complexes are precipitated using a specific antibody against the target protein; after reversing the crosslinks, the purified DNA is analyzed by PCR, qPCR, or sequencing (ChIP-seq) to identify the DNA sequences bound by the target protein;\n"
            "③ DNase I footprinting: an in vitro assay in which the test DNA is end-labeled, incubated with protein, and then partially digested with DNase I; the DNA region protected by bound protein is not cleaved by DNase I, and after electrophoresis a blank 'footprint' region appears, allowing precise localization of the protein-binding DNA site at single-nucleotide resolution."
        ),
    }
    T["short-answer-7-q-032"] = {
        "prompt": "Functions of protein tags in gene expression vectors",
        "referenceAnswer": (
            "① Affinity purification: His tag (6 histidines) enables purification of recombinant proteins by nickel ion affinity chromatography; GST tag enables purification by glutathione affinity chromatography; MBP tag enables purification by maltose affinity chromatography;\n"
            "② Protein detection: fluorescent tags such as GFP and RFP allow direct observation of protein localization and dynamic changes in cells; small tags such as Flag, HA, and Myc can be detected using commercially available specific antibodies for Western blot, immunofluorescence, immunoprecipitation, and other assays;\n"
            "③ Improving protein expression level and solubility: fusion tags such as MBP, GST, and NusA can improve the solubility of heterologously expressed proteins, promote proper folding, and reduce inclusion body formation;\n"
            "④ Protein interaction studies: tags are used for Co-IP, Pull-down, and other experiments to study protein-protein interactions;\n"
            "⑤ Protein localization studies: fluorescent tags or organelle localization signal tags can be used to study the subcellular localization of proteins."
        ),
    }
    T["short-answer-7-q-033"] = {
        "prompt": "Three cloning methods for inserting a gene of interest into a plasmid",
        "referenceAnswer": (
            "① Restriction enzyme digestion and ligation method:"
        ),
    }
    T["short-answer-7-q-034"] = {
        "prompt": "Principle: using the same or compatible restriction endonucleases to digest both the gene of interest and the plasmid vector, generating complementary sticky ends, and then ligating them with T4 DNA ligase;",
        "referenceAnswer": (
            "Features: the method is classical and well-established; using two different restriction enzymes enables directional cloning, avoiding reverse insertion of the gene of interest and vector self-ligation; however, it is limited by the availability of restriction sites. "
            "② Seamless homologous recombination cloning method:"
        ),
    }
    T["short-answer-7-q-035"] = {
        "prompt": "Principle: sequences homologous to the linearized vector ends (15-40 bp) are designed at both ends of the gene of interest, and in vitro recombinases (such as Gibson Assembly, In-Fusion) catalyze recombination between the homologous sequences, achieving seamless insertion of the gene of interest;",
        "referenceAnswer": (
            "Features: does not depend on restriction enzyme recognition sites, leaves no extra bases after assembly; can simultaneously assemble multiple fragments; suitable for high-throughput cloning and complex vector construction. "
            "③ Gateway site-specific recombination cloning method:"
        ),
    }
    T["short-answer-7-q-036"] = {
        "prompt": "Principle: using the site-specific recombination system of bacteriophage lambda, the gene of interest is first cloned into an entry vector, and then transferred to various destination vectors through the LR recombination reaction;",
        "referenceAnswer": (
            "Features: no restriction digestion or ligation required; enables rapid transfer of the gene of interest between different vectors; suitable for large-scale functional genomics studies."
        ),
    }
    T["short-answer-7-q-037"] = {
        "prompt": "Experimental steps for seamless cloning",
        "referenceAnswer": (
            "① Primer design: add sequences homologous to the linearized vector ends (15-40 bp) to the 5' ends of both the forward and reverse primers of the gene of interest, so that the amplified gene has overlapping regions with the vector at both ends;\n"
            "② PCR amplification of the gene of interest: amplify the gene using the designed primers and purify the PCR product, ensuring no non-specific amplification;\n"
            "③ Preparation of linearized vector: linearize the plasmid vector using restriction endonucleases or PCR, and purify the linearized vector;\n"
            "④ Seamless assembly reaction: mix the linearized vector and the gene of interest at a molar ratio of 1:3 to 1:5, add the seamless cloning enzyme mix (containing 5' exonuclease, DNA polymerase, and DNA ligase), and incubate at 50°C for 15-60 minutes;\n"
            "⑤ Transformation and screening: transform the reaction product into competent E. coli and plate on medium containing the appropriate antibiotic for culture;\n"
            "⑥ Identification: pick single colonies and verify the correctness of the recombinant plasmid by PCR, restriction digestion, and sequencing."
        ),
    }
    T["short-answer-7-q-038"] = {
        "prompt": "Basic workflow of homologous recombination experiments (using gene knockout as an example)",
        "referenceAnswer": (
            "① Construction of homologous recombination vector: design and construct a targeting vector containing the upstream and downstream homology arms (500-2000 bp) of the target gene, with a selectable marker gene (such as the Neo resistance gene) and a negative selection marker (such as the TK gene) inserted between the homology arms;\n"
            "② Vector delivery: introduce the linearized targeting vector into recipient cells (such as mouse ES cells) by electroporation, microinjection, or other methods;\n"
            "③ Homologous recombination occurs: the cell uses its own homologous recombination machinery to recombine the targeting vector with the target gene locus in the genome via the homology arms, replacing the target gene with the selectable marker gene;\n"
            "④ Positive recombinant screening: select cells stably integrating the Neo gene by culturing in medium containing G418; further select cells that have undergone homologous recombination using ganciclovir (randomly integrated cells retain the TK gene and are killed by ganciclovir);\n"
            "⑤ Recombinant identification: verify whether correct homologous recombination has occurred by PCR, Southern blot, and sequencing, and obtain homozygous cells with the target gene knocked out."
        ),
    }
    T["short-answer-7-q-039"] = {
        "prompt": "Principles for selecting appropriate restriction endonucleases for gene insertion and the use of isocaudomers",
        "referenceAnswer": (
            "Principles for restriction enzyme selection: ① Choose enzyme recognition sites present in the multiple cloning site (MCS) of the plasmid; "
            "② Choose enzyme recognition sites present at both ends of the gene of interest but absent within the gene itself, to avoid cutting the gene of interest; "
            "③ Preferably choose enzymes that generate sticky ends to improve ligation efficiency; "
            "④ Choose two different enzyme recognition sites to achieve directional insertion of the gene of interest while preventing vector self-ligation; "
            "⑤ Avoid using enzymes that generate blunt ends, as blunt-end ligation efficiency is lower."
        ),
    }
    T["short-answer-7-q-040"] = {
        "prompt": "Guidelines for using isocaudomers:",
        "referenceAnswer": (
            "Isocaudomers are restriction endonucleases that recognize different sequences but generate the same sticky ends after cleavage "
            "(e.g., Sal I recognizes GTCGAC, Xho I recognizes CTCGAG, and both generate a 5'-TCGA-3' sticky end)."
        ),
    }
    T["short-answer-7-q-041"] = {
        "prompt": "Advantages: when the gene of interest contains commonly used restriction sites internally, isocaudomers can be used for cloning; directional insertion can be achieved; the ligated sequence is no longer recognized by the original two enzymes, preventing re-cleavage of the vector and insert and improving clone stability;",
        "referenceAnswer": (
            "Disadvantages: the ligated sequence can no longer be cleaved by the original enzymes, making it unsuitable for subsequent subcloning.\n\n"
            "Precautions: isocaudomer ligation alters the original restriction sites; when designing primers, the impact on the protein coding sequence must be considered."
        ),
    }
    T["short-answer-8-q-042"] = {
        "prompt": "Steps of Southern blotting",
        "referenceAnswer": (
            "① Genomic DNA digestion: digest genomic DNA with restriction endonucleases to produce fragments of appropriate sizes;\n"
            "② Gel electrophoresis: separate the digested DNA fragments by agarose gel electrophoresis;\n"
            "③ Denaturation and transfer: denature the DNA in the gel into single strands using NaOH solution, then transfer the DNA to a nylon or nitrocellulose membrane by capillary transfer or electrotransfer;\n"
            "④ Prehybridization: incubate the membrane in prehybridization solution to block non-specific binding sites;\n"
            "⑤ Hybridization: add a labeled specific DNA probe and hybridize to the DNA on the membrane;\n"
            "⑥ Washing: wash away unbound free probe from the membrane;\n"
            "⑦ Detection: detect specific bands according to the labeling method of the probe (radioisotope, fluorescence, or chemiluminescence)."
        ),
    }
    T["short-answer-8-q-043"] = {
        "prompt": "Steps of Northern blotting",
        "referenceAnswer": (
            "① Total RNA extraction: extract high-quality total RNA from tissues or cells;\n"
            "② Denaturing gel electrophoresis: separate RNA in a denaturing agarose gel containing formaldehyde to prevent RNA secondary structure formation;\n"
            "③ Transfer: transfer the RNA from the gel to a nylon membrane;\n"
            "④ Prehybridization and hybridization: same as Southern blot, hybridize with a labeled DNA or RNA probe;\n"
            "⑤ Washing and detection: same as Southern blot, detect the size and abundance of specific mRNA bands."
        ),
    }
    T["short-answer-8-q-044"] = {
        "prompt": "Steps of Western blotting",
        "referenceAnswer": (
            "① Protein sample preparation: extract total protein from tissues or cells and determine protein concentration;\n"
            "② SDS-PAGE electrophoresis: separate protein samples by SDS-polyacrylamide gel electrophoresis according to molecular weight;\n"
            "③ Transfer: transfer the proteins from the gel to a PVDF or nitrocellulose membrane;\n"
            "④ Blocking: block non-specific binding sites on the membrane with non-fat milk or BSA solution;\n"
            "⑤ Primary antibody incubation: incubate with a specific primary antibody against the target protein overnight at 4°C;\n"
            "⑥ Washing: wash away unbound primary antibody;\n"
            "⑦ Secondary antibody incubation: incubate with an HRP- or fluorophore-labeled secondary antibody for 1 hour at room temperature;\n"
            "⑧ Washing and detection: wash away unbound secondary antibody and detect protein bands by chemiluminescence or fluorescence."
        ),
    }
    T["short-answer-8-q-045"] = {
        "prompt": "Three methods for measuring RNA expression levels and their advantages and disadvantages",
        "referenceAnswer": (
            "① Quantitative real-time PCR (qRT-PCR):"
        ),
    }
    T["short-answer-8-q-046"] = {
        "prompt": "Principle: uses fluorescent signals to monitor the PCR amplification process in real time and performs relative quantification of RNA expression levels through Ct value analysis;",
        "referenceAnswer": (
            "Steps: extract total RNA → reverse transcribe to cDNA → design specific primers → perform fluorescence quantitative PCR → analyze results using the ΔΔCt method;"
        ),
    }
    T["short-answer-8-q-047"] = {
        "prompt": "Advantages: high sensitivity, strong specificity, rapid operation, relatively low cost, suitable for expression analysis of known genes in a large number of samples;",
        "referenceAnswer": (
            "Disadvantages: can only detect known genes and cannot discover new transcripts; only a few genes can be tested per experiment. "
            "② Northern blot:"
        ),
    }
    T["short-answer-8-q-048"] = {
        "prompt": "Principle: detects RNA expression levels and molecular weight through hybridization between RNA and a complementary probe;",
        "referenceAnswer": (
            "Advantages: can simultaneously obtain information on RNA expression level and molecular weight; high specificity and can detect alternative splicing variants;"
        ),
    }
    T["short-answer-8-q-049"] = {
        "prompt": "Disadvantages: low sensitivity, requires large amounts of RNA; complex and time-consuming operation; cannot achieve high-throughput detection.",
        "referenceAnswer": (
            "③ RNA sequencing (RNA-seq):"
        ),
    }
    T["short-answer-8-q-050"] = {
        "prompt": "Principle: uses high-throughput sequencing technology to sequence all RNAs in a sample and calculates gene expression levels by aligning to a reference genome;",
        "referenceAnswer": (
            "Steps: extract total RNA → construct cDNA library → high-throughput sequencing → data analysis;"
        ),
    }
    T["short-answer-8-q-051"] = {
        "prompt": "Advantages: comprehensively analyzes the entire transcriptome; can discover new genes, transcripts, and alternative splicing; wide quantitative range;",
        "referenceAnswer": (
            "Disadvantages: high cost; complex data analysis; high requirements for sample quality."
        ),
    }
    T["short-answer-8-q-052"] = {
        "prompt": "Basic operational steps of yeast two-hybrid (Y2H) screening",
        "referenceAnswer": (
            "① Vector construction: clone the bait protein gene into a vector containing the DNA-binding domain (BD) (such as pGBKT7) to construct the bait plasmid; clone the prey protein gene or cDNA library into a vector containing the transcription activation domain (AD) (such as pGADT7) to construct the prey plasmid;\n"
            "② Autoactivation test: transform the bait plasmid alone into yeast and test whether it can autoactivate reporter genes, excluding autoactivating baits;\n"
            "③ Co-transformation: co-transform the bait plasmid and prey plasmid into an auxotrophic yeast strain (such as AH109);\n"
            "④ Primary screening: plate the transformed yeast on double-dropout medium (SD/-Leu/-Trp) to select successfully transformed yeast;\n"
            "⑤ Secondary screening: replica-plate colonies from the double-dropout plate onto triple-dropout (SD/-Leu/-Trp/-His) or quadruple-dropout (SD/-Leu/-Trp/-His/-Ade) medium to select positive clones that activate reporter genes;\n"
            "⑥ Verification: further verify positive clones by the LacZ colorimetric assay; extract yeast plasmids and identify the interacting proteins by sequencing;\n"
            "⑦ Control experiments: set up blank controls and negative controls to exclude false-positive results."
        ),
    }
    T["short-answer-9-q-053"] = {
        "prompt": "Commonly used bacterium for introducing plasmids into plant cells and the relevant key DNA segments",
        "referenceAnswer": (
            "Commonly used bacterium: Agrobacterium tumefaciens, a soil Gram-negative bacterium that naturally possesses the ability to transfer its own DNA into plant cells."
        ),
    }
    T["short-answer-9-q-054"] = {
        "prompt": "Key transfer segments: T-DNA (transfer DNA) region on the Ti plasmid (tumor-inducing plasmid):",
        "referenceAnswer": (
            "① T-DNA: the DNA fragment that is transferred and integrated into the plant genome; its ends are the 25 bp left and right border sequences (LB/RB), which are essential signals for T-DNA transfer;\n"
            "② vir region (virulence region): located on the Ti plasmid, encodes a series of proteins required for T-DNA transfer (e.g., VirD2 cleaves the T-DNA borders, VirE2 protects single-stranded T-DNA), but the vir region itself does not enter plant cells;\n"
            "③ Modern binary vector system: the Ti plasmid is engineered into two independent plasmids: a mini-Ti plasmid (containing the T-DNA borders and gene of interest) and a helper plasmid (containing the vir region), improving the safety and efficiency of genetic transformation."
        ),
    }
    T["short-answer-9-q-055"] = {
        "prompt": "Common methods for introducing genes into host cells",
        "referenceAnswer": (
            "① Heat shock method: mix the plasmid with competent E. coli and apply a 42°C heat shock for 90 seconds to increase cell membrane permeability, allowing the plasmid to enter the cells; suitable for bacterial transformation;\n"
            "② Electroporation: uses high-voltage electrical pulses to create transient micropores in the cell membrane, allowing DNA to enter cells; suitable for bacteria, yeast, animal cells, and plant cells;\n"
            "③ Liposome transfection: DNA is encapsulated by cationic liposomes to form liposome-DNA complexes that enter cells through membrane fusion; suitable for transient transfection of animal cells;\n"
            "④ Microinjection: uses a micromanipulator to directly inject DNA into the cell nucleus; suitable for animal fertilized eggs and embryonic stem cells;\n"
            "⑤ Gene gun method: DNA is coated onto gold or tungsten microparticles and accelerated into cells or tissues using high-pressure gas; suitable for plant cells and difficult-to-transfect animal cells;\n"
            "⑥ Agrobacterium-mediated method: exploits the natural transformation ability of Agrobacterium to transfer the gene of interest on T-DNA into plant cells; the most commonly used method for plant genetic transformation."
        ),
    }
    T["short-answer-10-q-056"] = {
        "prompt": "All methods for achieving loss-of-function in reverse genetics",
        "referenceAnswer": (
            "① RNA interference (RNAi): introduce siRNA, shRNA, or miRNA to specifically degrade target mRNA and inhibit gene expression;\n"
            "② CRISPR/Cas9 gene knockout: use Cas9 nuclease to create DNA double-strand breaks at the target gene locus; repair through non-homologous end joining (NHEJ) introduces frameshift mutations, leading to loss of gene function;\n"
            "③ Homologous recombination-directed knockout: replace the target gene with a selectable marker gene through homologous recombination, achieving complete gene knockout;\n"
            "④ T-DNA insertional inactivation: Agrobacterium-mediated random T-DNA insertion into the plant genome disrupts gene function at the insertion site;\n"
            "⑤ Transposon insertional inactivation: exploit the random transposition of transposons to insert into genes and cause gene inactivation;\n"
            "⑥ Point mutation inactivation: introduce stop codons or critical amino acid mutations within the gene using overlap extension PCR or megaprimer mutagenesis to render the protein non-functional;\n"
            "⑦ Antisense RNA technology: express antisense RNA complementary to target mRNA to inhibit its translation."
        ),
    }
    T["short-answer-10-q-057"] = {
        "prompt": "Design an experiment to locate intron positions within the gene corresponding to a cDNA sequence",
        "referenceAnswer": (
            "Experimental principle: cDNA is reverse-transcribed from mature mRNA and therefore does not contain introns; genomic DNA contains both exons and introns. By comparing the PCR product sizes or sequences from both templates, the positions and sizes of introns can be determined."
        ),
    }
    T["short-answer-10-q-058"] = {
        "prompt": "Experimental method 1: Genomic DNA vs. cDNA PCR comparison",
        "referenceAnswer": (
            "① Extract genomic DNA and total RNA from the species of interest;\n"
            "② Reverse-transcribe total RNA into cDNA;\n"
            "③ Design multiple primer pairs based on the known cDNA sequence to cover the entire cDNA region;\n"
            "④ Perform PCR amplification using genomic DNA and cDNA as templates, respectively;\n"
            "⑤ Compare the sizes of amplification products by agarose gel electrophoresis: if the genomic DNA product is larger than the cDNA product, the fragment contains an intron, and the size difference corresponds to the intron length;\n"
            "⑥ Sequence both PCR products and compare the sequences to precisely determine intron boundaries (conforming to the GT-AG rule) and sizes."
        ),
    }
    T["short-answer-10-q-059"] = {
        "prompt": "Experimental method 2: Bioinformatics alignment",
        "referenceAnswer": (
            "① If the genome sequence of the species has been determined, use the cDNA sequence as a query to align against the reference genome using tools such as BLAST or Splign;\n"
            "② Regions where the alignment is interrupted correspond to introns, and their precise positions and sizes can be directly obtained;\n"
            "③ Verify the predicted intron boundaries by RT-PCR and sequencing.\n\n"
            "Supplementary validation: analyze RNA-seq data to examine read coverage at splice junctions, confirming the presence of introns and splicing patterns."
        ),
    }
    T["short-answer-10-q-060"] = {
        "prompt": "Given a chemically induced single-gene mutant phenotype, how to design an experiment to clone the mutated gene? (Map-based cloning)",
        "referenceAnswer": (
            "Map-based cloning is a gene cloning method based on genetic linkage analysis that does not require prior knowledge of the gene sequence:\n"
            "① Construct a mapping population: cross the mutant (e.g., obtained by EMS mutagenesis) with a wild-type strain of a distinct genetic background to obtain the F1 generation; self the F1 to obtain an F2 segregating population, or backcross to the mutant to obtain a BC1 population;\n"
            "② Screen individuals with the mutant phenotype: select individuals exhibiting the mutant phenotype from the F2 or BC1 population for linkage analysis;\n"
            "③ Initial mapping: genotype the mutant individuals using molecular markers distributed across the entire genome (such as SSR, SNP, and Indel markers), identify molecular markers tightly linked to the mutant phenotype, and localize the mutant gene to a specific chromosomal segment;\n"
            "④ Fine mapping: develop additional molecular markers within the initially mapped region, expand the mapping population, screen recombinants, and progressively narrow the candidate interval (typically to tens or even a few kb);\n"
            "⑤ Candidate gene analysis: examine the genome annotation within the mapped interval and identify all possible candidate genes;\n"
            "⑥ Mutation site identification: PCR-amplify and sequence the candidate genes, compare the sequences between the mutant and wild type, and identify the nucleotide change (such as point mutation, deletion, or insertion) responsible for the mutant phenotype;\n"
            "⑦ Functional validation:"
        ),
    }
    T["short-answer-10-q-061"] = {
        "prompt": "Complementation test: introduce the wild-type candidate gene into the mutant; if the mutant phenotype is rescued, this proves that the gene is the causative gene;",
        "referenceAnswer": (
            "Reverse validation: knock out the gene in a wild-type background using CRISPR/Cas9 technology; if the same phenotype as the mutant appears, this further confirms the gene's function."
        ),
    }

    # =========================================================================
    # ESSAY (18 questions)
    # =========================================================================
    T["essay-1-q-001"] = {
        "prompt": "Alternative splicing verification problem: A gene has 4 exons, exon1=500 bp, exon2=200 bp, exon3=200 bp, exon4=300 bp. Exon2 undergoes alternative splicing and may produce two transcripts: 1-2-3-4 and 1-3-4. Calculate the transcript lengths and design an experiment to verify the existence of alternative splicing.",
        "referenceAnswer": (
            "Transcript length calculation: ① Transcript 1-2-3-4 containing all exons: 500+200+200+300 = 1200 bp; "
            "② Splicing variant 1-3-4 skipping exon2: 500+200+300 = 1000 bp."
        ),
    }
    T["essay-1-q-002"] = {
        "prompt": "Complete experimental validation protocol:",
        "referenceAnswer": (
            "① RNA extraction and reverse transcription: extract total RNA from tissues or cells with high expression of the gene, treat with DNase I to remove genomic DNA contamination, and then reverse-transcribe to cDNA;\n"
            "② Primer design: design a pair of specific PCR primers upstream of exon1 and downstream of exon4, with primers spanning more than one exon to avoid amplifying genomic DNA;\n"
            "③ RT-PCR amplification: perform PCR amplification using cDNA as template, including a no-template control and a genomic DNA control;\n"
            "④ Electrophoresis detection: run the PCR products on an agarose gel; two clear bands of approximately 1200 bp and 1000 bp are expected;\n"
            "⑤ Sequencing verification: excise and purify the two bands separately and sequence them; compare the sequencing results to confirm that the 1000 bp band indeed lacks the exon2 sequence and that the splice boundaries conform to the GT-AG rule;\n"
            "⑥ Quantitative verification (optional): design specific qPCR primers spanning the exon1-exon2 and exon1-exon3 splice junctions to quantitatively analyze the expression levels of the two transcripts in different tissues or under different treatment conditions;\n"
            "⑦ High-throughput verification (optional): perform RNA-seq analysis to examine the distribution of reads at splice junctions and verify the existence of alternative splicing at the whole-transcriptome level."
        ),
    }
    T["essay-2-q-003"] = {
        "prompt": "What is a telomere? Briefly describe the three main functions of telomeres. What enzyme catalyzes telomere synthesis?",
        "referenceAnswer": (
            "Definition: Telomeres are specialized DNA-protein complexes at the ends of eukaryotic linear chromosomes, composed of G-rich tandem repeat DNA sequences (TTAGGG in humans) and various telomere-binding proteins. Telomeres do not encode proteins and are essential for maintaining genome stability and integrity."
        ),
    }
    T["essay-2-q-004"] = {
        "prompt": "Three main functions:",
        "referenceAnswer": (
            "① Protection of chromosome ends: the specialized structures of telomeres (T-loop, D-loop) and their binding proteins seal the chromosome ends, preventing degradation by intracellular nucleases and avoiding abnormal end-to-end fusion, rearrangement, and circularization, thereby maintaining genome stability;\n"
            "② Solving the end-replication problem of linear DNA: DNA polymerase can only synthesize DNA in the 5'→3' direction and requires an RNA primer; therefore, it cannot replicate the very ends of linear chromosomes, causing telomeres to shorten with each cell division; telomeres serve as a 'buffer sequence' at chromosome ends, protecting internal coding genes from being lost;\n"
            "③ Regulating cellular senescence and proliferation: telomere length gradually shortens with increasing numbers of cell divisions; when telomeres shorten to a critical length, they trigger a DNA damage response, causing cells to enter replicative senescence or programmed cell death; telomere length is an important marker of the cellular 'division clock'; in embryonic stem cells, germ cells, and cancer cells, telomerase is activated to maintain telomere length, endowing cells with unlimited proliferative capacity."
        ),
    }
    T["essay-2-q-005"] = {
        "prompt": "The enzyme that catalyzes telomere synthesis: Telomerase, a specialized reverse transcriptase composed of a protein subunit (TERT) and an RNA template subunit (TERC); telomerase uses its own RNA as a template to add telomeric repeat sequences to chromosome ends, extending telomere length.",
        "referenceAnswer": "",
    }
    T["essay-3-q-006"] = {
        "prompt": "Describe the attenuation control of the trp operon with reference to the accompanying figure (see attached diagram)",
        "referenceAnswer": (
            "The attenuation control of the tryptophan (trp) operon is a fine-tuned transcriptional regulatory mechanism that couples the translation status of the leader peptide with changes in mRNA secondary structure to achieve precise regulation of tryptophan biosynthetic gene expression."
        ),
    }
    T["essay-3-q-007"] = {
        "prompt": "Figure a: Tryptophan starvation state",
        "referenceAnswer": (
            "When the intracellular tryptophan concentration is extremely low, the level of Trp-tRNAtrp is insufficient, and the ribosome stalls during translation of the leader peptide at the consecutive tryptophan codons (UGGUGG); at this point, the ribosome occupies region 1 of the leader sequence, allowing regions 2 and 3 to pair and form an anti-termination stem-loop structure; region 4 cannot pair with region 3, so a terminator structure cannot form; RNA polymerase can continue transcribing the downstream tryptophan biosynthetic structural genes to synthesize tryptophan to meet cellular demand."
        ),
    }
    T["essay-3-q-008"] = {
        "prompt": "Figure b: Tryptophan abundance state",
        "referenceAnswer": (
            "When the intracellular tryptophan concentration is sufficient, the level of Trp-tRNAtrp is abundant, and the ribosome can smoothly translate the leader peptide and dissociate at the stop codon; at this point, the ribosome occupies regions 1 and 2 of the leader sequence, allowing regions 3 and 4 to pair and form a strong terminator stem-loop structure; the stretch of U residues downstream of the terminator causes RNA polymerase to dissociate from the DNA template, terminating transcription prematurely and stopping the expression of tryptophan biosynthetic genes to avoid wasting amino acids."
        ),
    }
    T["essay-3-q-009"] = {
        "prompt": "Two-tier regulatory mechanism of the tryptophan (trp) operon",
        "referenceAnswer": (
            "The tryptophan operon is a classic negatively regulated operon in prokaryotes that precisely regulates tryptophan synthesis through two tiers of control: repressor regulation and attenuation regulation."
        ),
    }
    T["essay-3-q-010"] = {
        "prompt": "First tier: Repressor regulation (coarse control)",
        "referenceAnswer": (
            "The repressor protein encoded by the trpR gene is inactive on its own and cannot bind to the operator sequence; when the intracellular tryptophan concentration is high, tryptophan acts as a corepressor and binds to the repressor protein, inducing a conformational change that activates it; the activated repressor binds to the operator sequence of the trp operon, blocking the progression of RNA polymerase and inhibiting transcription initiation; when the tryptophan concentration is low, the corepressor dissociates, the repressor returns to its inactive state and dissociates from the operator, and transcription is turned on."
        ),
    }
    T["essay-3-q-011"] = {
        "prompt": "Second tier: Attenuation regulation (fine control)",
        "referenceAnswer": (
            "Repressor regulation can only control whether transcription initiates, whereas attenuation regulation can finely tune the efficiency of transcription termination after initiation, based on the intracellular tryptophan concentration; it controls the secondary structure of mRNA through the translation status of the leader peptide, determining whether transcription terminates prematurely (see previous question for details)."
        ),
    }
    T["essay-3-q-012"] = {
        "prompt": "Synergistic effect: Repressor regulation and attenuation regulation work synergistically, enabling the expression of the trp operon to respond rapidly and precisely to changes in intracellular tryptophan concentration, maintaining stable intracellular tryptophan levels.",
        "referenceAnswer": "",
    }
    T["essay-4-q-013"] = {
        "prompt": "Similarities and differences in cytoplasmic gene expression between prokaryotes (bacteria) and eukaryotes (humans)",
        "referenceAnswer": (
            "Similarities: ① The core chemical mechanism of translation is highly conserved; both use mRNA as a template, tRNA as amino acid carriers, and ribosomes as the translational machinery to catalyze peptide bond formation; "
            "② Both follow the universal genetic code (with a few exceptions in mitochondrial codons); "
            "③ The translation process is divided into three stages—initiation, elongation, and termination—all requiring elongation factors and release factors; "
            "④ Both possess regulatory mechanisms at the translation level, such as mRNA stability regulation and translation initiation regulation.\n\n"
            "Differences: ① Spatiotemporal coupling:"
        ),
    }
    T["essay-4-q-014"] = {
        "prompt": "Prokaryotes: transcription and translation occur simultaneously; while mRNA is still being transcribed, ribosomes already bind to the mRNA and begin translation;",
        "referenceAnswer": (
            "Eukaryotes: transcription occurs in the nucleus; after processing (capping, polyadenylation, splicing, etc.), mRNA is transported through nuclear pores to the cytoplasm before translation begins; transcription and translation are completely separated in time and space. "
            "② mRNA structural features:"
        ),
    }
    T["essay-4-q-015"] = {
        "prompt": "Prokaryotes: mRNA is mostly polycistronic, with one mRNA encoding multiple functionally related proteins; each ORF has an independent upstream SD sequence; mRNA half-life is short, typically only a few minutes;",
        "referenceAnswer": (
            "Eukaryotes: mRNA is mostly monocistronic, with one mRNA encoding only one protein; it has a 5' cap structure and a 3' poly(A) tail, and its half-life is longer, ranging from minutes to days. "
            "③ Translation initiation mechanism:"
        ),
    }
    T["essay-4-q-016"] = {
        "prompt": "Prokaryotes: the ribosome is directly positioned at the start codon through complementary base pairing between the SD sequence and 16S rRNA; the initiating amino acid is fMet; there are only three initiation factors;",
        "referenceAnswer": (
            "Eukaryotes: the ribosome binds to the 5' cap structure of mRNA and then scans to find the AUG start codon; the initiating amino acid is Met; there are more than ten initiation factors, and the process is more complex. "
            "④ Ribosome structure:"
        ),
    }
    T["essay-4-q-017"] = {
        "prompt": "Prokaryotes: 70S ribosome, composed of a 30S small subunit and a 50S large subunit;",
        "referenceAnswer": (
            "Eukaryotes: 80S ribosome, composed of a 40S small subunit and a 60S large subunit. "
            "⑤ Post-translational modifications:"
        ),
    }
    T["essay-4-q-018"] = {
        "prompt": "Prokaryotes: post-translational modifications are relatively few, primarily simple cleavage and phosphorylation;",
        "referenceAnswer": (
            "Eukaryotes: post-translational modifications are complex and diverse, including glycosylation, phosphorylation, ubiquitination, acetylation, and cleavage, and are crucial for protein function and localization."
        ),
    }

    return T


def apply_translations():
    """Read the question bank, apply translations, and write it back."""
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    translations = build_translations()

    updated = 0
    skipped = 0
    for q in data["questions"]:
        qid = q["id"]
        if q["type"] == "translation":
            skipped += 1
            continue
        if qid not in translations:
            print(f"  WARNING: No translation for {qid}")
            continue
        t = translations[qid]

        # Translate prompt
        if "prompt" in t:
            q["prompt"] = t["prompt"]

        # Translate explanation (true-false, multiple-choice)
        if "explanation" in t:
            q["explanation"] = t["explanation"]

        # Translate referenceAnswer (short-answer, essay)
        if "referenceAnswer" in t:
            q["referenceAnswer"] = t["referenceAnswer"]

        updated += 1

    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Updated {updated} questions, skipped {skipped} translation questions")
    return data, updated, skipped


def verify(data):
    """Print the first 3 translated prompts of each type."""
    for qtype in ["true-false", "multiple-choice", "short-answer", "essay"]:
        print(f"\n{'='*60}")
        print(f"  TYPE: {qtype}")
        print(f"{'='*60}")
        count = 0
        for q in data["questions"]:
            if q["type"] == qtype:
                print(f"\n  [{q['id']}]")
                print(f"  Prompt: {q.get('prompt','')[:120]}")
                if "explanation" in q:
                    print(f"  Explanation: {q['explanation'][:120]}...")
                if "referenceAnswer" in q and q["referenceAnswer"]:
                    ra = q["referenceAnswer"]
                    print(f"  ReferenceAnswer: {ra[:120]}...")
                count += 1
                if count >= 3:
                    break
        if count == 0:
            print("  (none found)")


if __name__ == "__main__":
    print("Applying translations...")
    data, updated, skipped = apply_translations()
    print("Verifying...")
    verify(data)
    print("\nDone.")
