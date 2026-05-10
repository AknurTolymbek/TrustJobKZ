import "./style.css";
import { useMemo, useState } from "react";

const pages = ["home", "detector", "resume", "skills", "analytics", "about"];

const copy = {
  en: {
    nav: {
      home: "Home",
      detector: "Detector",
      resume: "Resume Match",
      skills: "Skill Gap",
      analytics: "Analytics",
      about: "About",
    },
    ready: "Ready",
    heroEyebrow: "AI vacancy trust screening",
    heroLead:
      "A calm, practical workspace for checking job posts before candidates spend time on risky applications.",
    checkVacancy: "Check vacancy",
    viewAnalytics: "View analytics",
    preview: "Live detector preview",
    cleanExample: "Clean vacancy",
    suspiciousExample: "Suspicious vacancy",
    detectorEyebrow: "Detector",
    detectorTitle: "Vacancy check",
    detectorText: "Paste the vacancy details and review the model result in one place.",
    fields: {
      url: "Vacancy URL",
      title: "Job title",
      location: "Location",
      salary: "Salary",
      company: "Company profile",
      employment: "Employment type",
      description: "Description",
      requirements: "Requirements",
      benefits: "Benefits",
    },
    placeholders: {
      url: "https://hh.kz/vacancy/...",
      title: "Frontend Developer",
      location: "Almaty",
      salary: "650000-900000 KZT",
      company: "Registered local company",
      employment: "Full-time, part-time, remote",
      description: "Paste the main vacancy text",
      requirements: "Experience, skills, documents, schedule",
      benefits: "Benefits, schedule, social package",
    },
    runCheck: "Run check",
    urlHint: "Paste a vacancy link for automatic extraction, or fill the form manually.",
    extractedFromUrl: "Extracted from URL",
    checking: "Checking...",
    noResult: "No result yet",
    noResultText: "The result summary will appear here after the check.",
    connectionIssue: "Connection issue",
    backendError: "Backend is not available. Start FastAPI on port 8000.",
    prediction: "Prediction",
    riskLevel: "Risk level",
    mlProbability: "ML probability",
    finalRiskScore: "Final risk score",
    noPhrases: "No suspicious phrases",
    recommendationsTitle: "Safer similar vacancies",
    recommendationsText: "Based on similar real vacancies from the Kazakhstan dataset.",
    openVacancy: "Open vacancy",
    noRecommendations: "No similar safe vacancies found yet.",
    resumeTitle: "Resume-to-job matching",
    resumeText: "Paste your resume and find real vacancies that best match your profile.",
    resumePlaceholder: "Example: I am an Information Systems student. I know SQL, Python, Excel, Power BI and data analysis.",
    findMatches: "Find matches",
    matching: "Matching...",
    resumeEmpty: "Matched jobs will appear here.",
    matchPercent: "Match",
    matchedSkills: "Matched skills",
    missingSkills: "Missing skills",
    skillGapTitle: "Skill gap analysis",
    skillGapText: "Compare your resume with a vacancy and see which skills are already covered and which ones are missing.",
    vacancyTitle: "Vacancy title",
    vacancyDescription: "Vacancy description",
    vacancyPlaceholder: "Paste vacancy requirements or choose a job from resume matches.",
    analyzeSkills: "Analyze skills",
    analyzing: "Analyzing...",
    skillGapEmpty: "Skill gap results will appear here.",
    coverage: "Coverage",
    resumeSkills: "Skills found in resume",
    requiredSkills: "Skills required by vacancy",
    features: [
      ["ML prediction", "Uses the trained TrustJobKZ model and local risk signals from the ML folder."],
      ["Candidate-first", "Highlights risk level, score, suspicious phrases and a short explanation."],
      ["Local workflow", "Runs against your FastAPI backend at 127.0.0.1:8000."],
    ],
    analyticsTitle: "Model overview",
    analyticsText: "A compact dashboard for explaining what the system considers during a vacancy review.",
    analyticsCards: [
      ["Signals", "13", "Text, missing fields and rule-based indicators"],
      ["Models", "2", "Text-only and hybrid models available in ML artifacts"],
      ["API", "1", "FastAPI endpoint used by the frontend detector"],
    ],
    riskComposition: "Risk composition",
    commonRiskMarkers: "Common risk markers",
    markers: [
      "Requests to move communication to messengers.",
      "Very high salary with vague job responsibilities.",
      "Missing company details, salary or requirements.",
      "Urgent language and promises without verification.",
    ],
    aboutTitle: "Built for safer job search in Kazakhstan",
    aboutText:
      "TrustJobKZ combines trained vacancy classification with transparent local rules so users can see why a post may be risky.",
    timeline: [
      ["Collect", "Vacancy fields are entered into the detector."],
      ["Predict", "The backend sends data through the ML predictor."],
      ["Explain", "The frontend shows score, risk and detected phrases."],
    ],
  },
  ru: {
    nav: {
      home: "Главная",
      detector: "Проверка",
      resume: "Резюме",
      skills: "Скиллы",
      analytics: "Аналитика",
      about: "О модели",
    },
    ready: "Готово",
    heroEyebrow: "AI-проверка безопасности вакансий",
    heroLead:
      "Спокойный и понятный сервис для проверки вакансий перед тем, как пользователь потратит время на рискованный отклик.",
    checkVacancy: "Проверить вакансию",
    viewAnalytics: "Открыть аналитику",
    preview: "Быстрая проверка",
    cleanExample: "Нормальная вакансия",
    suspiciousExample: "Подозрительная вакансия",
    detectorEyebrow: "Детектор",
    detectorTitle: "Проверка вакансии",
    detectorText: "Вставьте данные вакансии и получите результат модели в одном месте.",
    fields: {
      url: "Ссылка на вакансию",
      title: "Название вакансии",
      location: "Город",
      salary: "Зарплата",
      company: "Профиль компании",
      employment: "Тип занятости",
      description: "Описание",
      requirements: "Требования",
      benefits: "Условия и бонусы",
    },
    placeholders: {
      url: "https://hh.kz/vacancy/...",
      title: "Frontend Developer",
      location: "Алматы",
      salary: "650000-900000 KZT",
      company: "Зарегистрированная локальная компания",
      employment: "Полная, частичная, удаленная",
      description: "Вставьте основной текст вакансии",
      requirements: "Опыт, навыки, документы, график",
      benefits: "Бонусы, график, соцпакет",
    },
    runCheck: "Запустить проверку",
    urlHint: "Вставьте ссылку на вакансию для автоматического анализа или заполните форму вручную.",
    extractedFromUrl: "Извлечено по ссылке",
    checking: "Проверяем...",
    noResult: "Результата пока нет",
    noResultText: "После проверки здесь появится итог модели.",
    connectionIssue: "Проблема подключения",
    backendError: "Backend недоступен. Запустите FastAPI на порту 8000.",
    prediction: "Прогноз",
    riskLevel: "Уровень риска",
    mlProbability: "Вероятность ML",
    finalRiskScore: "Итоговый риск",
    noPhrases: "Подозрительные фразы не найдены",
    recommendationsTitle: "Похожие безопасные вакансии",
    recommendationsText: "Подобраны по похожести среди реальных вакансий из Kazakhstan dataset.",
    openVacancy: "Открыть вакансию",
    noRecommendations: "Похожие безопасные вакансии пока не найдены.",
    resumeTitle: "Подбор вакансий по резюме",
    resumeText: "Вставьте резюме, и система найдёт реальные вакансии, которые лучше всего подходят профилю.",
    resumePlaceholder: "Пример: Я студент Information Systems. Знаю SQL, Python, Excel, Power BI и анализ данных.",
    findMatches: "Найти вакансии",
    matching: "Ищем...",
    resumeEmpty: "Подходящие вакансии появятся здесь.",
    matchPercent: "Совпадение",
    matchedSkills: "Совпавшие скиллы",
    missingSkills: "Не хватает",
    skillGapTitle: "Skill gap анализ",
    skillGapText: "Сравните резюме с вакансией и посмотрите, какие навыки уже есть, а каких не хватает.",
    vacancyTitle: "Название вакансии",
    vacancyDescription: "Описание вакансии",
    vacancyPlaceholder: "Вставьте требования вакансии или выберите вакансию из подбора.",
    analyzeSkills: "Проверить скиллы",
    analyzing: "Анализируем...",
    skillGapEmpty: "Результат skill gap появится здесь.",
    coverage: "Покрытие",
    resumeSkills: "Скиллы в резюме",
    requiredSkills: "Скиллы в вакансии",
    features: [
      ["ML-прогноз", "Использует обученную модель TrustJobKZ и локальные risk signals из ML-папки."],
      ["Понятно для пользователя", "Показывает риск, score, подозрительные фразы и короткое объяснение."],
      ["Локальный workflow", "Работает через FastAPI backend на 127.0.0.1:8000."],
    ],
    analyticsTitle: "Обзор модели",
    analyticsText: "Краткий dashboard о том, какие сигналы учитывает система при проверке вакансии.",
    analyticsCards: [
      ["Сигналы", "13", "Текст, пропущенные поля и rule-based признаки"],
      ["Модели", "2", "Text-only и hybrid модели в ML artifacts"],
      ["API", "1", "FastAPI endpoint для frontend detector"],
    ],
    riskComposition: "Состав риска",
    commonRiskMarkers: "Частые признаки риска",
    markers: [
      "Просьба перейти в мессенджеры.",
      "Очень высокая зарплата при неясных обязанностях.",
      "Нет информации о компании, зарплате или требованиях.",
      "Срочность и обещания без подтверждений.",
    ],
    aboutTitle: "Для более безопасного поиска работы в Казахстане",
    aboutText:
      "TrustJobKZ объединяет ML-классификацию вакансий и прозрачные локальные правила, чтобы пользователь видел, почему объявление может быть рискованным.",
    timeline: [
      ["Сбор", "Пользователь вводит данные вакансии."],
      ["Прогноз", "Backend отправляет данные в ML predictor."],
      ["Объяснение", "Frontend показывает score, риск и найденные фразы."],
    ],
  },
  kz: {
    nav: {
      home: "Басты",
      detector: "Тексеру",
      resume: "Түйіндеме",
      skills: "Дағдылар",
      analytics: "Аналитика",
      about: "Модель",
    },
    ready: "Дайын",
    heroEyebrow: "AI арқылы вакансия қауіпсіздігін тексеру",
    heroLead:
      "Үміткер күмәнді вакансияға уақыт жұмсамай тұрып, хабарландыруды тез әрі түсінікті тексеруге арналған сервис.",
    checkVacancy: "Вакансияны тексеру",
    viewAnalytics: "Аналитиканы ашу",
    preview: "Жылдам тексеру",
    cleanExample: "Қалыпты вакансия",
    suspiciousExample: "Күмәнді вакансия",
    detectorEyebrow: "Детектор",
    detectorTitle: "Вакансияны тексеру",
    detectorText: "Вакансия мәліметтерін енгізіп, модель нәтижесін бір жерден көріңіз.",
    fields: {
      url: "Вакансия сілтемесі",
      title: "Вакансия атауы",
      location: "Қала",
      salary: "Жалақы",
      company: "Компания туралы",
      employment: "Жұмыс түрі",
      description: "Сипаттама",
      requirements: "Талаптар",
      benefits: "Шарттар мен бонус",
    },
    placeholders: {
      url: "https://hh.kz/vacancy/...",
      title: "Frontend Developer",
      location: "Алматы",
      salary: "650000-900000 KZT",
      company: "Тіркелген жергілікті компания",
      employment: "Толық, жартылай, қашықтан",
      description: "Вакансия мәтінін енгізіңіз",
      requirements: "Тәжірибе, дағдылар, құжаттар, кесте",
      benefits: "Бонус, жұмыс кестесі, әлеуметтік пакет",
    },
    runCheck: "Тексеруді бастау",
    urlHint: "Автоматты талдау үшін вакансия сілтемесін енгізіңіз немесе форманы қолмен толтырыңыз.",
    extractedFromUrl: "Сілтемеден алынған",
    checking: "Тексерілуде...",
    noResult: "Әзірге нәтиже жоқ",
    noResultText: "Тексеруден кейін модель қорытындысы осында шығады.",
    connectionIssue: "Қосылу қатесі",
    backendError: "Backend қолжетімсіз. FastAPI-ді 8000 портында іске қосыңыз.",
    prediction: "Болжам",
    riskLevel: "Қауіп деңгейі",
    mlProbability: "ML ықтималдығы",
    finalRiskScore: "Жалпы қауіп",
    noPhrases: "Күмәнді сөздер табылмады",
    recommendationsTitle: "Ұқсас қауіпсіз вакансиялар",
    recommendationsText: "Kazakhstan dataset ішіндегі нақты вакансияларға ұқсастық бойынша таңдалды.",
    openVacancy: "Вакансияны ашу",
    noRecommendations: "Ұқсас қауіпсіз вакансиялар әзірге табылмады.",
    resumeTitle: "Түйіндеме бойынша вакансия табу",
    resumeText: "Түйіндемеңізді енгізіңіз, жүйе профиліңізге сәйкес нақты вакансияларды табады.",
    resumePlaceholder: "Мысалы: Мен Information Systems студентімін. SQL, Python, Excel, Power BI және data analysis білемін.",
    findMatches: "Вакансияларды табу",
    matching: "Ізделуде...",
    resumeEmpty: "Сәйкес вакансиялар осында шығады.",
    matchPercent: "Сәйкестік",
    matchedSkills: "Сәйкес дағдылар",
    missingSkills: "Жетпейтін дағдылар",
    skillGapTitle: "Skill gap талдауы",
    skillGapText: "Түйіндемені вакансиямен салыстырып, қандай дағдылар бар және қандайы жетіспейтінін көріңіз.",
    vacancyTitle: "Вакансия атауы",
    vacancyDescription: "Вакансия сипаттамасы",
    vacancyPlaceholder: "Вакансия талаптарын енгізіңіз немесе резюме подборынан вакансия таңдаңыз.",
    analyzeSkills: "Дағдыларды талдау",
    analyzing: "Талдануда...",
    skillGapEmpty: "Skill gap нәтижесі осында шығады.",
    coverage: "Қамту",
    resumeSkills: "Түйіндемедегі дағдылар",
    requiredSkills: "Вакансия талап ететін дағдылар",
    features: [
      ["ML-болжам", "TrustJobKZ үйретілген моделін және ML-папкадағы жергілікті risk signals қолданады."],
      ["Пайдаланушыға түсінікті", "Risk, score, күмәнді сөздер және қысқа түсіндіру көрсетеді."],
      ["Локалды workflow", "FastAPI backend арқылы 127.0.0.1:8000 мекенжайында жұмыс істейді."],
    ],
    analyticsTitle: "Модельге шолу",
    analyticsText: "Вакансияны тексеру кезінде жүйе қандай сигналдарды ескеретінін көрсететін қысқа dashboard.",
    analyticsCards: [
      ["Сигналдар", "13", "Мәтін, бос өрістер және rule-based белгілер"],
      ["Модельдер", "2", "ML artifacts ішіндегі text-only және hybrid модельдер"],
      ["API", "1", "Frontend detector қолданатын FastAPI endpoint"],
    ],
    riskComposition: "Қауіп құрамы",
    commonRiskMarkers: "Жиі кездесетін қауіп белгілері",
    markers: [
      "Мессенджерге өтуді сұрау.",
      "Міндеттері түсініксіз, бірақ жалақысы өте жоғары ұсыныс.",
      "Компания, жалақы немесе талаптар туралы ақпараттың болмауы.",
      "Дәлелсіз шұғылдық және тым тартымды уәделер.",
    ],
    aboutTitle: "Қазақстанда қауіпсіз жұмыс іздеу үшін",
    aboutText:
      "TrustJobKZ ML-классификация мен ашық жергілікті ережелерді біріктіріп, вакансия неге қауіпті болуы мүмкін екенін түсіндіреді.",
    timeline: [
      ["Жинау", "Пайдаланушы вакансия мәліметтерін енгізеді."],
      ["Болжам", "Backend деректерді ML predictor-ға жібереді."],
      ["Түсіндіру", "Frontend score, risk және табылған сөздерді көрсетеді."],
    ],
  },
};

const initialForm = {
  job_url: "",
  title: "",
  company_profile: "",
  description: "",
  requirements: "",
  benefits: "",
  salary_range: "",
  location: "",
  employment_type: "",
};

const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

const examples = [
  {
    label: { en: "Clean vacancy", ru: "Нормальная вакансия", kz: "Қалыпты вакансия" },
    title: "Frontend Developer",
    description:
      "We are looking for a React developer to join our product team in Almaty.",
    requirements: "React, JavaScript, REST API experience, teamwork.",
    benefits: "Flexible schedule and professional development.",
    salary_range: "650000-900000 KZT",
    location: "Almaty",
    employment_type: "Full-time",
    company_profile: "A registered technology company with an office team.",
  },
  {
    label: { en: "Suspicious vacancy", ru: "Подозрительная вакансия", kz: "Күмәнді вакансия" },
    title: "Remote assistant",
    description:
      "Urgent work from home. High salary, no experience. Contact via WhatsApp.",
    requirements: "Start today.",
    benefits: "",
    salary_range: "",
    location: "Remote",
    employment_type: "Remote",
    company_profile: "",
  },
];

function App() {
  const [activePage, setActivePage] = useState("home");
  const [language, setLanguage] = useState("en");
  const [form, setForm] = useState(initialForm);
  const [result, setResult] = useState(null);
  const [isChecking, setIsChecking] = useState(false);
  const [error, setError] = useState("");
  const [resumeText, setResumeText] = useState("");
  const [resumeMatches, setResumeMatches] = useState([]);
  const [isMatching, setIsMatching] = useState(false);
  const [matchError, setMatchError] = useState("");
  const [skillForm, setSkillForm] = useState({
    resume_text: "",
    job_title: "",
    job_description: "",
    job_url: "",
  });
  const [skillGap, setSkillGap] = useState(null);
  const [isAnalyzingSkills, setIsAnalyzingSkills] = useState(false);
  const [skillError, setSkillError] = useState("");

  const resultTone = useMemo(() => {
    if (!result) return "neutral";
    if (result.prediction === "Fake") return "danger";
    if (result.prediction === "Suspicious" || result.risk_level === "Medium") {
      return "warning";
    }
    return "success";
  }, [result]);
  const t = copy[language];

  function goTo(page) {
    setActivePage(page);
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  function updateField(event) {
    const { name, value } = event.target;
    setForm((current) => ({ ...current, [name]: value }));
  }

  function loadExample(example) {
    const { label, ...exampleForm } = example;
    void label;
    setForm({ ...initialForm, ...exampleForm });
    setResult(null);
    setError("");
    goTo("detector");
  }

  async function checkJob(event) {
    event.preventDefault();
    setIsChecking(true);
    setError("");
    setResult(null);

    try {
      const endpoint = form.job_url.trim() ? "predict-url" : "predict";
      const payload = form.job_url.trim()
        ? { url: form.job_url.trim() }
        : form;

      const response = await fetch(`${API_URL}/${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error("Backend returned an error");
      }

      const dataResult = await response.json();
      setResult(dataResult);
    } catch {
      setError(t.backendError);
    } finally {
      setIsChecking(false);
    }
  }

  async function matchResume(event) {
    event.preventDefault();
    setIsMatching(true);
    setMatchError("");
    setResumeMatches([]);

    try {
      const response = await fetch(`${API_URL}/resume-match`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ resume_text: resumeText, limit: 5 }),
      });

      if (!response.ok) {
        throw new Error("Backend returned an error");
      }

      const data = await response.json();
      setResumeMatches(data.matches || []);
    } catch {
      setMatchError(t.backendError);
    } finally {
      setIsMatching(false);
    }
  }

  function updateSkillField(event) {
    const { name, value } = event.target;
    setSkillForm((current) => ({ ...current, [name]: value }));
  }

  function selectJobForSkillGap(job) {
    setSkillForm({
      resume_text: resumeText,
      job_title: job.title,
      job_description: "",
      job_url: job.url,
    });
    setSkillGap(null);
    setSkillError("");
    goTo("skills");
  }

  async function analyzeSkillGap(event) {
    event.preventDefault();
    setIsAnalyzingSkills(true);
    setSkillError("");
    setSkillGap(null);

    try {
      const response = await fetch(`${API_URL}/skill-gap`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(skillForm),
      });

      if (!response.ok) {
        throw new Error("Backend returned an error");
      }

      const data = await response.json();
      setSkillGap(data);
    } catch {
      setSkillError(t.backendError);
    } finally {
      setIsAnalyzingSkills(false);
    }
  }

  return (
    <div className="app-shell">
      <header className="topbar">
        <button className="brand" onClick={() => goTo("home")}>
          <span className="brand-mark">TJ</span>
          <span>TrustJobKZ</span>
        </button>

        <nav className="nav-links" aria-label="Main navigation">
          {pages.map((page) => (
            <button
              key={page}
              className={activePage === page ? "active" : ""}
              onClick={() => goTo(page)}
            >
              {t.nav[page]}
            </button>
          ))}
        </nav>

        <div className="language-switch" aria-label="Language switcher">
          <button
            className={language === "en" ? "active" : ""}
            onClick={() => setLanguage("en")}
          >
            EN
          </button>
          <button
            className={language === "ru" ? "active" : ""}
            onClick={() => setLanguage("ru")}
          >
            RU
          </button>
          <button
            className={language === "kz" ? "active" : ""}
            onClick={() => setLanguage("kz")}
          >
            KZ
          </button>
        </div>
      </header>

      <main>
        {activePage === "home" && (
          <HomePage goTo={goTo} loadExample={loadExample} language={language} t={t} />
        )}
        {activePage === "detector" && (
          <DetectorPage
            language={language}
            t={t}
            form={form}
            result={result}
            resultTone={resultTone}
            error={error}
            isChecking={isChecking}
            updateField={updateField}
            checkJob={checkJob}
            loadExample={loadExample}
          />
        )}
        {activePage === "resume" && (
          <ResumePage
            t={t}
            resumeText={resumeText}
            setResumeText={setResumeText}
            resumeMatches={resumeMatches}
            isMatching={isMatching}
            error={matchError}
            matchResume={matchResume}
            selectJobForSkillGap={selectJobForSkillGap}
          />
        )}
        {activePage === "skills" && (
          <SkillGapPage
            t={t}
            skillForm={skillForm}
            skillGap={skillGap}
            isAnalyzingSkills={isAnalyzingSkills}
            error={skillError}
            updateSkillField={updateSkillField}
            analyzeSkillGap={analyzeSkillGap}
          />
        )}
        {activePage === "analytics" && <AnalyticsPage t={t} />}
        {activePage === "about" && <AboutPage goTo={goTo} t={t} />}
      </main>
    </div>
  );
}

function HomePage({ goTo, loadExample, language, t }) {
  return (
    <section className="hero-section">
      <div className="hero-copy">
        <p className="eyebrow">{t.heroEyebrow}</p>
        <h1>TrustJobKZ</h1>
        <p className="hero-lead">{t.heroLead}</p>
        <div className="hero-actions">
          <button className="primary-btn" onClick={() => goTo("detector")}>
            {t.checkVacancy}
          </button>
          <button className="secondary-btn" onClick={() => goTo("analytics")}>
            {t.viewAnalytics}
          </button>
        </div>
      </div>

      <aside className="hero-panel">
        <div className="panel-header">
          <span>{t.preview}</span>
          <span className="status-dot">{t.ready}</span>
        </div>
        <div className="preview-stack">
          {examples.map((example) => (
            <button
              className="preview-card"
              key={example.label.en}
              onClick={() => loadExample(example)}
            >
              <span>{example.label[language]}</span>
              <strong>{example.title}</strong>
              <small>{example.location || "No location"}</small>
            </button>
          ))}
        </div>
      </aside>

      <div className="feature-grid">
        {t.features.map(([title, text]) => (
          <FeatureCard key={title} title={title} text={text} />
        ))}
      </div>
    </section>
  );
}

function DetectorPage({
  language,
  t,
  form,
  result,
  resultTone,
  error,
  isChecking,
  updateField,
  checkJob,
  loadExample,
}) {
  const isUrlMode = Boolean(form.job_url.trim());

  return (
    <section className="page-section detector-layout">
      <div className="section-heading">
        <p className="eyebrow">{t.detectorEyebrow}</p>
        <h2>{t.detectorTitle}</h2>
        <p>{t.detectorText}</p>
      </div>

      <form className="detector-form" onSubmit={checkJob}>
        <label>
          {t.fields.url}
          <input
            name="job_url"
            value={form.job_url}
            onChange={updateField}
            placeholder={t.placeholders.url}
          />
          <span className="field-hint">{t.urlHint}</span>
        </label>

        <div className="form-grid">
          <label>
            {t.fields.title}
            <input
              name="title"
              value={form.title}
              onChange={updateField}
              placeholder={t.placeholders.title}
              required={!isUrlMode}
            />
          </label>
          <label>
            {t.fields.location}
            <input
              name="location"
              value={form.location}
              onChange={updateField}
              placeholder={t.placeholders.location}
            />
          </label>
          <label>
            {t.fields.salary}
            <input
              name="salary_range"
              value={form.salary_range}
              onChange={updateField}
              placeholder={t.placeholders.salary}
            />
          </label>
          <label>
            {t.fields.company}
            <input
              name="company_profile"
              value={form.company_profile}
              onChange={updateField}
              placeholder={t.placeholders.company}
            />
          </label>
          <label>
            {t.fields.employment}
            <input
              name="employment_type"
              value={form.employment_type}
              onChange={updateField}
              placeholder={t.placeholders.employment}
            />
          </label>
        </div>

        <label>
          {t.fields.description}
          <textarea
            name="description"
            value={form.description}
            onChange={updateField}
            placeholder={t.placeholders.description}
            required={!isUrlMode}
          />
        </label>

        <label>
          {t.fields.requirements}
          <textarea
            name="requirements"
            value={form.requirements}
            onChange={updateField}
            placeholder={t.placeholders.requirements}
          />
        </label>

        <label>
          {t.fields.benefits}
          <textarea
            name="benefits"
            value={form.benefits}
            onChange={updateField}
            placeholder={t.placeholders.benefits}
          />
        </label>

        <div className="form-actions">
          <button className="primary-btn" disabled={isChecking}>
            {isChecking ? t.checking : t.runCheck}
          </button>
          {examples.map((example) => (
            <button
              className="ghost-btn"
              key={example.label.en}
              onClick={() => loadExample(example)}
              type="button"
            >
              {example.label[language]}
            </button>
          ))}
        </div>
      </form>

      <aside className={`result-panel ${result ? resultTone : ""}`}>
        {!result && !error && (
          <div className="empty-state">
            <span className="score-ring">--</span>
            <h3>{t.noResult}</h3>
            <p>{t.noResultText}</p>
          </div>
        )}

        {error && (
          <div className="empty-state error-state">
            <span className="score-ring">!</span>
            <h3>{t.connectionIssue}</h3>
            <p>{error}</p>
          </div>
        )}

        {result && (
          <>
            <div className="result-topline">
              <span>{t.prediction}</span>
              <strong>{result.prediction}</strong>
            </div>
            <div className="score-block">
              <span className="score-ring">{result.suspicion_score}</span>
              <div>
                <p>{t.riskLevel}</p>
                <h3>{result.risk_level}</h3>
              </div>
            </div>
            <div className="metric-row">
              <span>{t.mlProbability}</span>
              <strong>{Math.round((result.ml_fraud_probability || 0) * 100)}%</strong>
            </div>
            <div className="metric-row">
              <span>{t.finalRiskScore}</span>
              <strong>{Math.round((result.final_risk_score || 0) * 100)}%</strong>
            </div>
            <p className="explanation">{result.explanation}</p>
            {result.extracted_job && (
              <div className="extracted-box">
                <span>{t.extractedFromUrl}</span>
                <strong>{result.extracted_job.title}</strong>
                <small>{result.source_url}</small>
              </div>
            )}
            <div className="tag-list">
              {(result.detected_phrases || []).length > 0 ? (
                result.detected_phrases.map((item) => (
                  <span className="tag" key={item}>
                    {item}
                  </span>
                ))
              ) : (
                <span className="tag muted">{t.noPhrases}</span>
              )}
            </div>
            <RecommendationList
              recommendations={result.recommendations || []}
              t={t}
            />
          </>
        )}
      </aside>
    </section>
  );
}

function RecommendationList({ recommendations, t }) {
  return (
    <div className="recommendations">
      <div>
        <h3>{t.recommendationsTitle}</h3>
        <p>{t.recommendationsText}</p>
      </div>

      {recommendations.length === 0 ? (
        <p className="muted-text">{t.noRecommendations}</p>
      ) : (
        <div className="recommendation-list">
          {recommendations.map((job) => (
            <article className="recommendation-card" key={`${job.title}-${job.url}`}>
              <strong>{job.title}</strong>
              <span>{job.company_name}</span>
              <small>{job.salary}</small>
              {job.url && (
                <a href={job.url} target="_blank" rel="noreferrer">
                  {t.openVacancy}
                </a>
              )}
            </article>
          ))}
        </div>
      )}
    </div>
  );
}

function ResumePage({
  t,
  resumeText,
  setResumeText,
  resumeMatches,
  isMatching,
  error,
  matchResume,
  selectJobForSkillGap,
}) {
  return (
    <section className="page-section tool-layout">
      <div className="section-heading">
        <p className="eyebrow">{t.nav.resume}</p>
        <h2>{t.resumeTitle}</h2>
        <p>{t.resumeText}</p>
      </div>

      <form className="tool-form" onSubmit={matchResume}>
        <label>
          Resume
          <textarea
            value={resumeText}
            onChange={(event) => setResumeText(event.target.value)}
            placeholder={t.resumePlaceholder}
            required
          />
        </label>
        <button className="primary-btn" disabled={isMatching}>
          {isMatching ? t.matching : t.findMatches}
        </button>
      </form>

      <aside className="tool-panel">
        {error && <p className="muted-text">{error}</p>}
        {!error && resumeMatches.length === 0 && (
          <div className="empty-state">
            <span className="score-ring">--</span>
            <h3>{t.resumeEmpty}</h3>
          </div>
        )}

        {resumeMatches.length > 0 && (
          <div className="match-list">
            {resumeMatches.map((job) => (
              <article className="match-card" key={`${job.title}-${job.url}`}>
                <div className="result-topline">
                  <span>{t.matchPercent}</span>
                  <strong>{job.match_percent}%</strong>
                </div>
                <h3>{job.title}</h3>
                <p>{job.company_name}</p>
                <small>{job.salary}</small>
                <SkillTags title={t.matchedSkills} items={job.matched_skills} />
                <SkillTags title={t.missingSkills} items={job.missing_skills} muted />
                <div className="form-actions">
                  {job.url && (
                    <a className="text-link" href={job.url} target="_blank" rel="noreferrer">
                      {t.openVacancy}
                    </a>
                  )}
                  <button
                    className="ghost-btn"
                    type="button"
                    onClick={() => selectJobForSkillGap(job)}
                  >
                    {t.analyzeSkills}
                  </button>
                </div>
              </article>
            ))}
          </div>
        )}
      </aside>
    </section>
  );
}

function SkillGapPage({
  t,
  skillForm,
  skillGap,
  isAnalyzingSkills,
  error,
  updateSkillField,
  analyzeSkillGap,
}) {
  return (
    <section className="page-section tool-layout">
      <div className="section-heading">
        <p className="eyebrow">{t.nav.skills}</p>
        <h2>{t.skillGapTitle}</h2>
        <p>{t.skillGapText}</p>
      </div>

      <form className="tool-form" onSubmit={analyzeSkillGap}>
        <label>
          Resume
          <textarea
            name="resume_text"
            value={skillForm.resume_text}
            onChange={updateSkillField}
            placeholder={t.resumePlaceholder}
            required
          />
        </label>
        <label>
          {t.vacancyTitle}
          <input
            name="job_title"
            value={skillForm.job_title}
            onChange={updateSkillField}
            placeholder={t.placeholders.title}
          />
        </label>
        <label>
          {t.vacancyDescription}
          <textarea
            name="job_description"
            value={skillForm.job_description}
            onChange={updateSkillField}
            placeholder={t.vacancyPlaceholder}
          />
        </label>
        <button className="primary-btn" disabled={isAnalyzingSkills}>
          {isAnalyzingSkills ? t.analyzing : t.analyzeSkills}
        </button>
      </form>

      <aside className="tool-panel">
        {error && <p className="muted-text">{error}</p>}
        {!error && !skillGap && (
          <div className="empty-state">
            <span className="score-ring">--</span>
            <h3>{t.skillGapEmpty}</h3>
          </div>
        )}

        {skillGap && (
          <div className="skill-gap-result">
            <div className="score-block">
              <span className="score-ring">{skillGap.coverage_percent}</span>
              <div>
                <p>{t.coverage}</p>
                <h3>{skillGap.job_title}</h3>
              </div>
            </div>
            <SkillTags title={t.resumeSkills} items={skillGap.resume_skills} />
            <SkillTags title={t.requiredSkills} items={skillGap.required_skills} />
            <SkillTags title={t.matchedSkills} items={skillGap.matched_skills} />
            <SkillTags title={t.missingSkills} items={skillGap.missing_skills} muted />
          </div>
        )}
      </aside>
    </section>
  );
}

function SkillTags({ title, items, muted = false }) {
  return (
    <div className="skill-tags">
      <span>{title}</span>
      <div className="tag-list">
        {(items || []).length > 0 ? (
          items.map((item) => (
            <span className={muted ? "tag muted" : "tag"} key={item}>
              {item}
            </span>
          ))
        ) : (
          <span className="tag muted">None</span>
        )}
      </div>
    </div>
  );
}

function AnalyticsPage({ t }) {
  return (
    <section className="page-section">
      <div className="section-heading wide">
        <p className="eyebrow">{t.nav.analytics}</p>
        <h2>{t.analyticsTitle}</h2>
        <p>{t.analyticsText}</p>
      </div>

      <div className="analytics-grid">
        {t.analyticsCards.map(([label, value, text]) => (
          <MetricCard key={label} label={label} value={value} text={text} />
        ))}
      </div>

      <div className="insight-layout">
        <div className="insight-panel">
          <h3>{t.riskComposition}</h3>
          <div className="bar-row">
            <span>ML probability</span>
            <div className="bar"><span style={{ width: "68%" }} /></div>
          </div>
          <div className="bar-row">
            <span>Local rules</span>
            <div className="bar accent"><span style={{ width: "42%" }} /></div>
          </div>
          <div className="bar-row">
            <span>Missing fields</span>
            <div className="bar warm"><span style={{ width: "54%" }} /></div>
          </div>
        </div>

        <div className="insight-panel">
          <h3>{t.commonRiskMarkers}</h3>
          <ul className="clean-list">
            {t.markers.map((marker) => (
              <li key={marker}>{marker}</li>
            ))}
          </ul>
        </div>
      </div>
    </section>
  );
}

function AboutPage({ goTo, t }) {
  return (
    <section className="page-section about-layout">
      <div className="section-heading">
        <p className="eyebrow">{t.nav.about}</p>
        <h2>{t.aboutTitle}</h2>
        <p>{t.aboutText}</p>
        <button className="primary-btn" onClick={() => goTo("detector")}>
          {t.checkVacancy}
        </button>
      </div>

      <div className="timeline">
        {t.timeline.map(([title, text]) => (
          <TimelineItem key={title} title={title} text={text} />
        ))}
      </div>
    </section>
  );
}

function FeatureCard({ title, text }) {
  return (
    <article className="feature-card">
      <h3>{title}</h3>
      <p>{text}</p>
    </article>
  );
}

function MetricCard({ label, value, text }) {
  return (
    <article className="metric-card">
      <span>{label}</span>
      <strong>{value}</strong>
      <p>{text}</p>
    </article>
  );
}

function TimelineItem({ title, text }) {
  return (
    <article className="timeline-item">
      <span>{title}</span>
      <p>{text}</p>
    </article>
  );
}

export default App;
