import { Language } from "../types/api";

export interface AppTranslations {
  // Navigation & Shell
  appName: string;
  appTagline: string;
  tabAdvice: string;
  tabHistory: string;
  tabReliability: string;
  tabHelp: string;
  settings: string;
  online: string;
  offline: string;

  // Language Picker
  chooseLanguage: string;
  langKn: string;
  langHi: string;
  langEn: string;

  // Welcome Screen
  welcomeTitle: string;
  welcomeSubtitle: string;
  welcomePromise: string;
  startBtn: string;

  // Honesty Banners & Badges
  syntheticBanner: string;
  demoNumbersBadge: string;
  lowConfidenceBadge: string;
  lowConfidenceReason: string;
  staleDataBanner: string;
  offlineBanner: string;
  disclaimer: string;
  sourceMeasured: string;
  sourceAssumption: string;

  // Stepper Header
  stepCounter: string;
  stepReviewTitle: string;
  nextBtn: string;
  backBtn: string;
  editLink: string;
  getAdviceBtn: string;
  calculatingAdvice: string;

  // Step 1: Crop
  stepCropTitle: string;
  stepCropDesc: string;
  cropOnion: string;
  cropOnionSub: string;
  cropPotato: string;
  cropTomato: string;
  comingSoon: string;

  // Step 2: Location
  stepLocationTitle: string;
  stepLocationDesc: string;
  useMyLocation: string;
  speakVillage: string;
  listening: string;
  selectMandiPlaceholder: string;
  mandiKolar: string;
  mandiChikkaballapur: string;
  mandiYeshwanthpur: string;

  // Step 3: Quantity
  stepQuantityTitle: string;
  stepQuantityDesc: string;
  totalVolume: string;
  quintalsUnit: string;
  bagConversion: string;

  // Step 4: Storage
  stepStorageTitle: string;
  stepStorageDesc: string;
  storageNoneTitle: string;
  storageNoneDesc: string;
  storageWarehouseTitle: string;
  storageWarehouseDesc: string;
  storageColdTitle: string;
  storageColdDesc: string;
  rotRiskHigh: string;
  rotRiskMedium: string;
  rotRiskLow: string;

  // Step 5: Trader Debt
  stepDebtTitle: string;
  stepDebtDesc: string;
  debtNo: string;
  debtNoDesc: string;
  debtYes: string;
  debtYesDesc: string;
  debtPrivate: string;
  debtPrivateDesc: string;
  whyWeAskTitle: string;
  whyWeAskDesc: string;

  // Step 6: Review Screen
  reviewSummaryHeading: string;
  reviewCropLabel: string;
  reviewLocationLabel: string;
  reviewQuantityLabel: string;
  reviewStorageLabel: string;
  reviewDebtLabel: string;

  // Results: Answer Card
  resultsTitle: string;
  readAloud: string;
  stopVoice: string;

  // Results: Where to Sell
  whereToSellTitle: string;
  whereToSellSubtitle: string;
  bestOptionBadge: string;
  priceYouMayGet: string;
  mostLikelyPrice: string;
  worstCasePrice: string;
  gainVsLocal: string;
  gainTotalLot: string;
  costsTakenOffTitle: string;
  transportCost: string;
  mandiFeesCommission: string;
  transitShrinkage: string;
  localMandiComparisonTitle: string;
  localMandiComparisonDesc: string;

  // Results: When to Sell
  whenToSellTitle: string;
  whenToSellSubtitle: string;
  sellTodayOption: string;
  waitDaysOption: string;
  chanceWaitingPays: string;
  expectedGainWait: string;
  worstCaseWait: string;

  // Results: Price Outlook Fan Chart
  chartTitle: string;
  chartSubtitle: string;
  axisPrice: string;
  axisDays: string;
  horizon7d: string;
  horizon14d: string;
  horizon30d: string;
  rangeLegend: string;
  medianLegend: string;

  // Results: Borrow Toggle
  borrowToggleTitle: string;
  borrowToggleDesc: string;
  borrowActiveStatus: string;
  borrowWarning: string;

  // Results: Storage Nearby
  storageNearbyTitle: string;
  storageNearbySubtitle: string;
  costPerDay: string;
  capacityText: string;
  callBtn: string;

  // Sharing & Feedback
  shareWhatsAppBtn: string;
  downloadSummaryBtn: string;
  savedToHistoryText: string;
  feedbackPrompt: string;
  feedbackHelpful: string;
  feedbackNotHelpful: string;
  feedbackThankYou: string;

  // History Screen
  historyTitle: string;
  historyEmpty: string;
  historyAdviceDate: string;
  historyRecommendedMandi: string;
  historyExpectedRange: string;
  actualPriceQuestion: string;
  saveActualPriceBtn: string;
  savedSuccess: string;

  // Reliability Screen
  reliabilityTitle: string;
  reliabilitySubtitle: string;
  trafficLightTitle: string;
  confidenceHigh: string;
  confidenceMedium: string;
  confidenceLow: string;
  baselineComparisonTitle: string;
  baselineComparisonDesc: string;
  colHorizon: string;
  colModelError: string;
  colSimpleGuessError: string;
  colOutcome: string;
  beatsSimpleGuess: string;
  doesNotBeatSimpleGuess: string;
  coverageTitle: string;
  coverageDesc: string;
  assumptionsTitle: string;
  assumptionsDesc: string;
  limitsTitle: string;

  // Help Screen
  helpTitle: string;
  helpSubtitle: string;
  howItWorksHeading: string;
  step1Text: string;
  step2Text: string;
  step3Text: string;
  boundariesHeading: string;
  boundariesBody: string;
  faqHeading: string;
  faq1Q: string;
  faq1A: string;
  faq2Q: string;
  faq2A: string;
  callHelperBtn: string;
  fieldFeedbackHeading: string;
  farmerNamePlaceholder: string;
  villagePlaceholder: string;
  notesPlaceholder: string;
  sendFeedbackBtn: string;

  // Settings
  settingsTitle: string;
  textSizeLabel: string;
  textSizeNormal: string;
  textSizeLarge: string;
  textSizeXLarge: string;
  darkModeLabel: string;
  voiceAudioLabel: string;
  startNewFarmerBtn: string;
  startNewFarmerDesc: string;
  clearDataBtn: string;
  closeBtn: string;

  // Crop Area & Supply Outlook
  tabCropArea: string;
  areaOutlookTitle: string;
  areaOutlookSubtitle: string;
  stepDistrictTitle: string;
  districtLabel: string;
  seasonLabel: string;
  yearLabel: string;
  stepAcresTitle: string;
  acresLabel: string;
  hectaresEquivalent: string;
  acresLimitHelp: string;
  voiceSpeakAcre: string;
  reportedByYouPrefix: string;
  stateAreaHeadline: string;
  cardDistrict: string;
  cardState: string;
  cardCountry: string;
  fiveYearAvg: string;
  signalHigher: string;
  signalNormal: string;
  signalLower: string;
  notAvailable: string;
  forecastsDisabledNotice: string;
  districtNotTrackedDisclaimer: string;
  reportedByFarmersStrip: string;
  farmerReportsCountLabel: string;
  coverageRatioLabel: string;
  tooFewReportsWarning: string;
  historyChartHeading: string;
  supplyPriceOutlookHeading: string;
  priceExpected30d: string;
  priceExpected60d: string;
  priceExpected90d: string;
  farmerAcreageIsolatedNote: string;
  officialSourceLabel: string;
  publishedOnLabel: string;
  seeCropAreaBtn: string;
  backToAdvisorBtn: string;
  submitAreaBtn: string;

  // Stitch AgroScan Advisor enhancements
  startNewFarmer: string;
  navEntry: string;
  navResults: string;
  navOfficer: string;
  navSources: string;
  navFeedback: string;
  liveKioskConnected: string;
  interactiveTestScenarios: string;
  scenarioNormal: string;
  scenarioFewReports: string;
  scenarioMissingOfficial: string;
  scenarioStaleData: string;
  scenarioHighSupply: string;
  kioskAssistedNote: string;
  shareWhatsApp: string;
  printPdf: string;
  fpoOfficerTitle: string;
  fpoOfficerSubtitle: string;
  exportCsvBtn: string;
  totalValidSubmissions: string;
  flaggedAnomalies: string;
  sourcesMethodsTitle: string;
  sourcesMethodsSubtitle: string;
  pillar1Title: string;
  pillar1Desc: string;
  pillar2Title: string;
  pillar2Desc: string;
  pillar3Title: string;
  pillar3Desc: string;
  feedbackHelpfulTitle: string;
  feedbackHelpfulSubtitle: string;
  feedbackYes: string;
  feedbackNo: string;
  recordAudioMemo: string;
  recentKioskReports: string;
  staleDataWarningNotice: string;

  // Stitch Farmer Sell Advisor UX System
  stationDepartment: string;
  kioskStation: string;
  jointAssistedMode: string;
  jointAssistedSub: string;
  liveMandiMapTitle: string;
  liveMandiMapRadius: string;
  tempoCalculatorTitle: string;
  tempoVehicleType: string;
  tempoTripEstimate: string;
  tempoNetGain: string;
  printSlipBtn: string;
  todayRealization: string;
  expectedRealizationWait: string;
  storageRotAllowance: string;
  rotAllowanceDeducted: string;
  bestValueBadge: string;
  highestSpotBadge: string;
  alternativeBadge: string;
  localMandiBadge: string;
  stepReviewSummary: string;
  stepReviewReady: string;
  stepReviewDirect: string;
  liveModalPrice: string;
  todayArrivals: string;
  estimatedLotValue: string;
  voiceGuidanceAvailable: string;
  voiceGuidanceSub: string;
  playAudio: string;
  youAreHere: string;
  distanceMarket: string;
  dispatchAdvisory: string;
  dispatchAdvisoryText: string;
}

export const translations: Record<Language, AppTranslations> = {
  // ================= KANNADA (Pure script - no mixed English/Hindi) =================
  /* needs native review */
  kn: {
    appName: "ರೈತ ಮಾರಾಟ ಸಲಹೆಗಾರ",
    appTagline: "ಕರ್ನಾಟಕದ ಈರುಳ್ಳಿ ಬೆಳೆಗಾರರಿಗೆ ಮಾರುಕಟ್ಟೆ ಮಾರ್ಗದರ್ಶಿ",
    tabAdvice: "ಮಾರಾಟ ಸಲಹೆ",
    tabHistory: "ನನ್ನ ಇತಿಹಾಸ",
    tabReliability: "ಎಷ್ಟು ನಂಬಿಕಸ್ಥ?",
    tabHelp: "ಸಹಾಯ",
    settings: "ಸೆಟ್ಟಿಂಗ್ಸ್",
    online: "ಆನ್‌ಲೈನ್",
    offline: "ಆಫ್‌ಲೈನ್",

    chooseLanguage: "ನಿಮ್ಮ ಭಾಷೆ ಆಯ್ಕೆ ಮಾಡಿ",
    langKn: "ಕನ್ನಡ",
    langHi: "हिन्दी",
    langEn: "English",

    welcomeTitle: "ಈರುಳ್ಳಿ ಮಾರಾಟಕ್ಕೆ ಸರಿಯಾದ ಸಮಯ ಮತ್ತು ಮಂಡಿ ಆಯ್ಕೆ",
    welcomeSubtitle: "ಮಂಡಿ ದರ, ಸಾಗಣೆ ವೆಚ್ಚ ಮತ್ತು ದಾಸ್ತಾನು ಲೆಕ್ಕಾಚಾರ ಮಾಡಿ ಹೆಚ್ಚು ಲಾಭ ಪಡೆಯಿರಿ.",
    welcomePromise: "ಸಂಪೂರ್ಣ ಉಚಿತ ಮತ್ತು ಪ್ರಾಮಾಣಿಕ ಸಲಹೆ",
    startBtn: "ಪ್ರಾರಂಭಿಸಿ",

    syntheticBanner: "ಕೃತಕ ಡೇಟಾ - ನೈಜ ನಿರ್ಧಾರಗಳಿಗೆ ಅಲ್ಲ: ಈ ಮಾದರಿಯನ್ನು ಪರೀಕ್ಷಾರ್ಥ ಡೇಟಾದ ಮೇಲೆ ಅಂದಾಜಿಸಲಾಗಿದೆ.",
    demoNumbersBadge: "ಪರೀಕ್ಷಾರ್ಥ ಸಂಖ್ಯೆಗಳು",
    lowConfidenceBadge: "ಕಡಿಮೆ ವಿಶ್ವಾಸಾರ್ಹತೆ",
    lowConfidenceReason: "ಈ ಅವಧಿಯ ಬೆಲೆ ಏರಿಳಿತ ಸಾಮಾನ್ಯಕ್ಕಿಂತ ಹೆಚ್ಚಾಗಿದೆ. ಎಚ್ಚರಿಕೆಯಿಂದ ನಿರ್ಧರಿಸಿ.",
    staleDataBanner: "ಹಳೆಯ ಡೇಟಾ: ಕೊನೆಯ ದಾಖಲೆ {date} ದಿನಾಂಕದ್ದು. ಮಾರುಕಟ್ಟೆಯಲ್ಲಿ ಖಚಿತಪಡಿಸಿಕೊಳ್ಳಿ.",
    offlineBanner: "ಇಂಟರ್ನೆಟ್ ಸಂಪರ್ಕವಿಲ್ಲ. ಉಳಿಸಿದ ಮಾಹಿತಿಯನ್ನು ತೋರಿಸಲಾಗುತ್ತಿದೆ.",
    disclaimer: "ಇದು ಕೇವಲ ಸಲಹೆ. ಅಂತಿಮ ನಿರ್ಧಾರ ನಿಮ್ಮದೇ.",
    sourceMeasured: "ನೈಜ ದರ",
    sourceAssumption: "ಅಂದಾಜು ವೆಚ್ಚ",

    stepCounter: "ಹಂತ {current} / {total}",
    stepReviewTitle: "ಮಾಹಿತಿ ಪರಿಶೀಲನೆ",
    nextBtn: "ಮುಂದೆ",
    backBtn: "ಹಿಂದೆ",
    editLink: "ಬದಲಾಯಿಸಿ",
    getAdviceBtn: "ಸಲಹೆ ಪಡೆಯಿರಿ",
    calculatingAdvice: "ಮಾರುಕಟ್ಟೆ ದರಗಳನ್ನು ಪರಿಶೀಲಿಸಲಾಗುತ್ತಿದೆ...",

    stepCropTitle: "ನಿಮ್ಮ ಬೆಳೆ ಯಾವುದು?",
    stepCropDesc: "ಇಂದು ಮಂಡಿ ಮುನ್ಸೂಚನೆ ಪಡೆಯಲು ನಿಮ್ಮ ಬೆಳೆಯನ್ನು ಆಯ್ಕೆ ಮಾಡಿ.",
    cropOnion: "ಈರುಳ್ಳಿ",
    cropOnionSub: "ರಬಿ ಮತ್ತು ಮುಂಗಾರು ಬೆಳೆ (ಸಕ್ರಿಯ ಮಾರುಕಟ್ಟೆ)",
    cropPotato: "ಆಲೂಗಡ್ಡೆ",
    cropTomato: "ಟೊಮೆಟೊ",
    comingSoon: "ಶೀಘ್ರದಲ್ಲೇ ಲಭ್ಯ",

    stepLocationTitle: "ನಿಮ್ಮ ಹತ್ತಿರದ ಮಂಡಿ ಯಾವುದು?",
    stepLocationDesc: "ಸಾರಿಗೆ ಮತ್ತು ಡೀಸೆಲ್ ವೆಚ್ಚ ಲೆಕ್ಕ ಹಾಕಲು ಸ್ಥಳ ಆರಿಸಿ.",
    useMyLocation: "ನನ್ನ ಸ್ಥಳ ಗುರುತಿಸಿ",
    speakVillage: "ಊರಿನ ಹೆಸರು ಹೇಳಿ",
    listening: "ಕೇಳಿಸಿಕೊಳ್ಳುತ್ತಿದ್ದೇವೆ... ಮಾತನಾಡಿ",
    selectMandiPlaceholder: "ಮಂಡಿ ಆಯ್ಕೆ ಮಾಡಿ",
    mandiKolar: "ಕೋಲಾರ ಮಂಡಿ",
    mandiChikkaballapur: "ಚಿಕ್ಕಬಳ್ಳಾಪುರ ಮಂಡಿ",
    mandiYeshwanthpur: "ಬೆಂಗಳೂರು ಯಶವಂತಪುರ ಮಂಡಿ",

    stepQuantityTitle: "ಮಾರಾಟಕ್ಕೆ ಎಷ್ಟು ಈರುಳ್ಳಿ ಇದೆ?",
    stepQuantityDesc: "ಕ್ವಿಂಟಾಲ್ ಲೆಕ್ಕದಲ್ಲಿ ಒಟ್ಟು ಪ್ರಮಾಣ ನಮೂದಿಸಿ.",
    totalVolume: "ಒಟ್ಟು ದಾಸ್ತಾನು",
    quintalsUnit: "ಕ್ವಿಂಟಾಲ್",
    bagConversion: "ಸುಮಾರು {bags} ಚೀಲಗಳು (ಪ್ರತಿ ಚೀಲ 50 ಕೆಜಿ)",

    stepStorageTitle: "ದಾಸ್ತಾನು ಸೌಲಭ್ಯ ಹೇಗಿದೆ?",
    stepStorageDesc: "ದಾಸ್ತಾನು ವಿಧಾನವು ಈರುಳ್ಳಿ ಕೊಳೆಯುವ ಪ್ರಮಾಣವನ್ನು ನಿರ್ಧರಿಸುತ್ತದೆ.",
    storageNoneTitle: "ಯಾವುದೇ ಸೌಲಭ್ಯವಿಲ್ಲ (ಬಯಲು)",
    storageNoneDesc: "ಬೇಗ ಮಾರಾಟ ಮಾಡುವುದು ಸೂಕ್ತ. ತಿಂಗಳಿಗೆ ಶೇ. 12 ರಷ್ಟು ತೂಕ ನಷ್ಟ.",
    storageWarehouseTitle: "ಸಾಮಾನ್ಯ ಗೋದಾಮು / ಕೊಟ್ಟಿಗೆ",
    storageWarehouseDesc: "ಗಾಳಿಯಾಡುವ ಶೆಡ್. 15 ರಿಂದ 20 ದಿನ ಸುರಕ್ಷಿತವಾಗಿ ಇಡಬಹುದು.",
    storageColdTitle: "ಶೀತಲ ಗೋದಾಮು (ಕೋಲ್ಡ್ ಸ್ಟೋರೇಜ್)",
    storageColdDesc: "ಉತ್ತಮ ರಕ್ಷಣೆ. ಗೋದಾಮು ರಸೀದಿ ಮೇಲೆ ಸಾಲ ಸೌಲಭ್ಯ ಲಭ್ಯ.",
    rotRiskHigh: "ಹೆಚ್ಚು ಕೊಳೆಯುವ ಅಪಾಯ (0-5 ದಿನ)",
    rotRiskMedium: "ಮಧ್ಯಮ ರಕ್ಷಣೆ (2-3 ವಾರ)",
    rotRiskLow: "ಕನಿಷ್ಠ ನಷ್ಟ (3 ತಿಂಗಳವರೆಗೆ)",

    stepDebtTitle: "ವ್ಯಾಪಾರಿಗೆ ಮುಂಗಡ ಸಾಲ ಕೊಡಬೇಕೆ?",
    stepDebtDesc: "ಕಮಿಷನ್ ಏಜೆಂಟ್ ಅಥವಾ ವ್ಯಾಪಾರಿಯಿಂದ ಮುಂಗಡ ಪಡೆದಿದ್ದೀರಾ?",
    debtNo: "ಇಲ್ಲ (ಯಾವುದೇ ಸಾಲವಿಲ್ಲ)",
    debtNoDesc: "ಎಲ್ಲಿ ಬೇಕಾದರೂ ಸ್ವತಂತ್ರವಾಗಿ ಮಾರಾಟ ಮಾಡಬಹುದು.",
    debtYes: "ಹೌದು (ಮುಂಗಡ ಸಾಲವಿದೆ)",
    debtYesDesc: "ಅದೇ ವ್ಯಾಪಾರಿಗೆ ಮಾರಾಟ ಮಾಡುವ ಬದ್ಧತೆ ಇರಬಹುದು.",
    debtPrivate: "ಹೇಳಲು ಇಷ್ಟವಿಲ್ಲ",
    debtPrivateDesc: "ಸಾಮಾನ್ಯ ಲೆಕ್ಕಾಚಾರ ತೋರಿಸಲಾಗುತ್ತದೆ.",
    whyWeAskTitle: "ಇದನ್ನು ಏಕೆ ಕೇಳುತ್ತಿದ್ದೇವೆ?",
    whyWeAskDesc: "ವ್ಯಾಪಾರಿಯ ಬಡ್ಡಿ ದರ ಹೆಚ್ಚಿದ್ದರೆ, ತಕ್ಷಣ ಮಾರಾಟ ಮಾಡುವುದು ಅಥವಾ ದಾಸ್ತಾನು ಇಡುವುದು ಯಾವುದು ಲಾಭ ಎಂದು ತಿಳಿಯಲು.",

    reviewSummaryHeading: "ನಿಮ್ಮ ವಿವರಗಳು ಸರಿಯಿವೆಯೇ ಪರಿಶೀಲಿಸಿ",
    reviewCropLabel: "ಬೆಳೆ",
    reviewLocationLabel: "ಲೋಡಿಂಗ್ ಮಂಡಿ",
    reviewQuantityLabel: "ಪ್ರಮಾಣ",
    reviewStorageLabel: "ದಾಸ್ತಾನು",
    reviewDebtLabel: "ವ್ಯಾಪಾರಿ ಸಾಲ",

    resultsTitle: "ನಿಮಗಾಗಿ ಮುಖ್ಯ ಸಲಹೆ",
    readAloud: "ಧ್ವನಿಯಲ್ಲಿ ಕೇಳಿ",
    stopVoice: "ಧ್ವನಿ ನಿಲ್ಲಿಸಿ",

    whereToSellTitle: "ಎಲ್ಲಿ ಮಾರಾಟ ಮಾಡಬೇಕು?",
    whereToSellSubtitle: "ಸಾಗಣೆ ಮತ್ತು ಕಮಿಷನ್ ಕಳೆದು ನಿಮ್ಮ ಕೈಗೆ ಸಿಗುವ ನಿವ್ವಳ ಹಣದ ಆಧಾರದಲ್ಲಿ ಶ್ರೇಯಾಂಕ",
    bestOptionBadge: "ಅತ್ಯುತ್ತಮ ಆಯ್ಕೆ",
    priceYouMayGet: "ನಿಮಗೆ ಸಿಗಬಹುದಾದ ಬೆಲೆ",
    mostLikelyPrice: "ಹೆಚ್ಚು ಸಂಭವನೀಯ ಬೆಲೆ",
    worstCasePrice: "ಕಡಿಮೆ ಮಾರುಕಟ್ಟೆ ಸಂದರ್ಭದಲ್ಲಿ",
    gainVsLocal: "ಸ್ಥಳೀಯ ಮಂಡಿಗಿಂತ ಸಿಗುವ ಲಾಭ",
    gainTotalLot: "ನಿಮ್ಮ ಒಟ್ಟು ದಾಸ್ತಾನಿಗೆ ಹೆಚ್ಚುವರಿ ಹಣ",
    costsTakenOffTitle: "ಕಳೆಯಲಾದ ವೆಚ್ಚಗಳು (ಸಾಗಣೆ, ಕಮಿಷನ್)",
    transportCost: "ಸಾರಿಗೆ ವೆಚ್ಚ",
    mandiFeesCommission: "ಮಂಡಿ ಶುಲ್ಕ ಮತ್ತು ಕಮಿಷನ್",
    transitShrinkage: "ದಾರಿಯಲ್ಲಿ ತೂಕದ ನಷ್ಟ",
    localMandiComparisonTitle: "ನಿಮ್ಮ ಸ್ಥಳೀಯ ಮಂಡಿ (ಹೋಲಿಕೆಗಾಗಿ ಮಾತ್ರ)",
    localMandiComparisonDesc: "ಬೇರೆ ಮಂಡಿಗೆ ಹೋಗಲು ತಗಲುವ ಸಾಗಣೆ ವೆಚ್ಚಕ್ಕಿಂತ ಹೆಚ್ಚಿನ ಬೆಲೆ ಸಿಗುತ್ತದೆಯೇ ಎಂದು ತಿಳಿಯಲು ಈ ಮಾನದಂಡ ನೋಡಿ.",

    whenToSellTitle: "ಯಾವಾಗ ಮಾರಾಟ ಮಾಡಬೇಕು?",
    whenToSellSubtitle: "ಇಂದೇ ಮಾರಾಟ ಮಾಡಬೇಕೆ ಅಥವಾ ಕಾಯಬೇಕೆ?",
    sellTodayOption: "ಇಂದೇ ಮಾರಾಟ ಮಾಡಿ",
    waitDaysOption: "{days} ದಿನ ಕಾಯಿರಿ",
    chanceWaitingPays: "ಕಾಯುವುದರಿಂದ ಲಾಭವಾಗುವ ಸಂಭವ",
    expectedGainWait: "ನಿರೀಕ್ಷಿತ ಹೆಚ್ಚುವರಿ ಲಾಭ",
    worstCaseWait: "ಕಾಯ್ದ ನಂತರ ಬೆಲೆ ಇಳಿದರೆ ಕೆಟ್ಟ ಪರಿಸ್ಥಿತಿ",

    chartTitle: "ಬೆಲೆ ಮುನ್ನೋಟ (ಮುಂದಿನ 30 ದಿನಗಳು)",
    chartSubtitle: "ಸಂಭಾವ್ಯ ಬೆಲೆಗಳ ಶ್ರೇಣಿ",
    axisPrice: "ದರ ಪ್ರತಿ ಕ್ವಿಂಟಾಲ್‌ಗೆ (ರೂ.)",
    axisDays: "ಇಂದಿನಿಂದ ದಿನಗಳು",
    horizon7d: "7 ದಿನ",
    horizon14d: "14 ದಿನ",
    horizon30d: "30 ದಿನ",
    rangeLegend: "ಬೆಲೆಯ ಸಂಭವನೀಯ ವ್ಯಾಪ್ತಿ",
    medianLegend: "ನಿರೀಕ್ಷಿತ ಸರಾಸರಿ ದರ",

    borrowToggleTitle: "ದಾಸ್ತಾನು ರಸೀದಿ ಮೇಲೆ ಸಾಲ ಪಡೆದರೆ?",
    borrowToggleDesc: "ಕಡಿಮೆ ಬಡ್ಡಿದರದ ಗೋದಾಮು ಸಾಲ ಪಡೆದಾಗ ನಿರ್ಧಾರ ಹೇಗೆ ಬದಲಾಗುತ್ತದೆ ನೋಡಿ.",
    borrowActiveStatus: "ಸಾಲ ಸೌಲಭ್ಯ ಪರಿಗಣಿಸಲಾಗಿದೆ",
    borrowWarning: "ಬೆಲೆ ಏರಿಕೆಯ ಲಾಭವು ಸಾಲದ ಬಡ್ಡಿಗಿಂತ ಹೆಚ್ಚಿದ್ದರೆ ಮಾತ್ರ ದಾಸ್ತಾನು ಇಡಿ.",

    storageNearbyTitle: "ಹತ್ತಿರದ ದಾಸ್ತಾನು ಸೌಲಭ್ಯಗಳು",
    storageNearbySubtitle: "ಈರುಳ್ಳಿ ಕೊಳೆಯದಂತೆ ಸುರಕ್ಷಿತವಾಗಿಡಲು ಆಯ್ಕೆಗಳು",
    costPerDay: "ಪ್ರತಿ ದಿನದ ಬಾಡಿಗೆ",
    capacityText: "ಸಾಮರ್ಥ್ಯ ಲಭ್ಯವಿದೆ",
    callBtn: "ಕರೆ ಮಾಡಿ",

    shareWhatsAppBtn: "ವಾಟ್ಸಾಪ್‌ನಲ್ಲಿ ಹಂಚಿಕೊಳ್ಳಿ",
    downloadSummaryBtn: "ವರದಿ ಡೌನ್‌ಲೋಡ್ ಮಾಡಿ",
    savedToHistoryText: "ನಿಮ್ಮ ಇತಿಹಾಸಕ್ಕೆ ಉಳಿಸಲಾಗಿದೆ",
    feedbackPrompt: "ಈ ಸಲಹೆ ನಿಮಗೆ ಉಪಯುಕ್ತವಾಯಿತೇ?",
    feedbackHelpful: "ಉಪಯುಕ್ತವಾಗಿದೆ",
    feedbackNotHelpful: "ಉಪಯುಕ್ತವಾಗಿಲ್ಲ",
    feedbackThankYou: "ನಿಮ್ಮ ಅನಿಸಿಕೆಗೆ ಧನ್ಯವಾದಗಳು!",

    historyTitle: "ಹಿಂದಿನ ಸಲಹೆಗಳು",
    historyEmpty: "ಇನ್ನೂ ಯಾವುದೇ ಸಲಹೆ ದಾಖಲಾಗಿಲ್ಲ. ಮುಖಪುಟದಿಂದ ಸಲಹೆ ಪಡೆಯಿರಿ.",
    historyAdviceDate: "ದಿನಾಂಕ",
    historyRecommendedMandi: "ಶಿಫಾರಸು ಮಾಡಿದ ಮಂಡಿ",
    historyExpectedRange: "ನಿರೀಕ್ಷಿತ ದರ ಶ್ರೇಣಿ",
    actualPriceQuestion: "ನಿಮಗೆ ಮಂಡಿಯಲ್ಲಿ ಸಿಕ್ಕ ನೈಜ ಬೆಲೆ ಎಷ್ಟು?",
    saveActualPriceBtn: "ನೈಜ ಬೆಲೆ ಉಳಿಸಿ",
    savedSuccess: "ಯಶಸ್ವಿಯಾಗಿ ಉಳಿಸಲಾಗಿದೆ!",

    reliabilityTitle: "ಈ ಸಲಹೆ ಎಷ್ಟು ನಂಬಿಕಸ್ಥ?",
    reliabilitySubtitle: "ನಾವು ಎಂದಿಗೂ ಒಂದೇ ನಿಶ್ಚಿತ ಬೆಲೆಯನ್ನು ಹೇಳುವುದಿಲ್ಲ. ಪ್ರತಿಯೊಂದು ಮುನ್ಸೂಚನೆಗೂ ಸಂಭವನೀಯ ವ್ಯಾಪ್ತಿ ಇರುತ್ತದೆ.",
    trafficLightTitle: "ಮುನ್ಸೂಚನೆ ನಿಖರತೆ ಸ್ಥಿತಿ",
    confidenceHigh: "ಉತ್ತಮ ವಿಶ್ವಾಸಾರ್ಹತೆ",
    confidenceMedium: "ಸಾಧಾರಣ ವಿಶ್ವಾಸಾರ್ಹತೆ",
    confidenceLow: "ಕಡಿಮೆ ವಿಶ್ವಾಸಾರ್ಹತೆ",
    baselineComparisonTitle: "ಸರಳ ಊಹೆಗೆ ಹೋಲಿಕೆ",
    baselineComparisonDesc: "ನಾಳಿನ ಬೆಲೆ ಇಂದಿನಷ್ಟೇ ಇರುತ್ತದೆ ಎಂಬ ಸರಳ ಊಹೆಗಿಂತ ನಮ್ಮ ಮಾದರಿ ಉತ್ತಮವೇ?",
    colHorizon: "ದಿನಗಳ ವ್ಯಾಪ್ತಿ",
    colModelError: "ಮಾದರಿಯ ಸರಾಸರಿ ವ್ಯತ್ಯಾಸ",
    colSimpleGuessError: "ಸರಳ ಊಹೆಯ ವ್ಯತ್ಯಾಸ",
    colOutcome: "ಫಲಿತಾಂಶ",
    beatsSimpleGuess: "ಮಾದರಿ ಉತ್ತಮವಾಗಿದೆ",
    doesNotBeatSimpleGuess: "ಸರಳ ಊಹೆಯೇ ಉತ್ತಮ",
    coverageTitle: "ಶ್ರೇಣಿಯ ಕವರೇಜ್ (ಗುರಿ 70-90%)",
    coverageDesc: "ನಿಜವಾದ ಬೆಲೆಯು ನಮ್ಮ ಅಂದಾಜಿನ ಶ್ರೇಣಿಯಲ್ಲಿ ಬರುವ ಪ್ರಮಾಣ.",
    assumptionsTitle: "ನೈಜ ಡೇಟಾ ಮತ್ತು ಅಂದಾಜುಗಳು",
    assumptionsDesc: "ಮಂಡಿ ದರಗಳು ಮತ್ತು ಹವಾಮಾನ ನೈಜವಾಗಿ ಅಳೆಯಲ್ಪಟ್ಟಿವೆ. ಸಾಗಣೆ ವೆಚ್ಚ ಮತ್ತು ಕಮಿಷನ್ ಶುಲ್ಕಗಳು ನಿಯಮಾವಳಿಗಳ ಆಧಾರದ ಮೇಲಿನ ಅಂದಾಜುಗಳು.",
    limitsTitle: "ತಿಳಿದಿರುವ ಮಿತಿಗಳು",

    helpTitle: "ಸಹಾಯ ಮತ್ತು ಬೆಂಬಲ",
    helpSubtitle: "ರೈತ ಮಾರಾಟ ಸಲಹೆಗಾರ ಹೇಗೆ ಕೆಲಸ ಮಾಡುತ್ತದೆ?",
    howItWorksHeading: "ಮೂರು ಸರಳ ಹಂತಗಳು",
    step1Text: "1. ನಿಮ್ಮ ಸ್ಥಳ, ಈರುಳ್ಳಿ ಪ್ರಮಾಣ ಮತ್ತು ದಾಸ್ತಾನು ವಿಧಾನ ತಿಳಿಸಿ.",
    step2Text: "2. ನಮ್ಮ ವ್ಯವಸ್ಥೆಯು ಕೋಲಾರ, ಯಶವಂತಪುರ ಮತ್ತು ಚಿಕ್ಕಬಳ್ಳಾಪುರ ಮಂಡಿಗಳ ದರ ಲೆಕ್ಕ ಹಾಕುತ್ತದೆ.",
    step3Text: "3. ಎಲ್ಲಿ ಮತ್ತು ಯಾವಾಗ ಮಾರಾಟ ಮಾಡಬೇಕೆಂದು ನೀವು ತೀರ್ಮಾನಿಸಿ.",
    boundariesHeading: "ನಮ್ಮ ಮಿತಿಗಳು ಮತ್ತು ಬದ್ಧತೆ",
    boundariesBody: "ನಾವು ಮಾರುಕಟ್ಟೆ ಮಾಹಿತಿ ನೀಡಿ ಸಲಹೆ ಮಾತ್ರ ನೀಡುತ್ತೇವೆ. ಅಂತಿಮ ವ್ಯಾಪಾರ ನಿರ್ಧಾರ ಸಂಪೂರ್ಣ ನಿಮ್ಮದೇ.",
    faqHeading: "ಸಾಮಾನ್ಯ ಪ್ರಶ್ನೆಗಳು",
    faq1Q: "ಇಲ್ಲಿ ತೋರಿಸುವ ಬೆಲೆ ಖಾತರಿಯೇ?",
    faq1A: "ಇಲ್ಲ. ಮಾರುಕಟ್ಟೆಯಲ್ಲಿ ಹರಾಜು ಪ್ರಕ್ರಿಯೆ ಇರುವುದರಿಂದ ಬೆಲೆಗಳಲ್ಲಿ ಏರಿಳಿತವಿರುತ್ತದೆ. ಆದ್ದರಿಂದ ನಾವು ಕನಿಷ್ಠ ಮತ್ತು ಗರಿಷ್ಠ ಶ್ರೇಣಿಯನ್ನು ಮಾತ್ರ ನೀಡುತ್ತೇವೆ.",
    faq2Q: "ದೂರದ ಮಂಡಿಗೆ ಹೋಗುವುದು ಯಾವಾಗ ಲಾಭದಾಯಕ?",
    faq2A: "ಹೆಚ್ಚುವರಿ ಬೆಲೆಯು ಸಾರಿಗೆ ವೆಚ್ಚ ಮತ್ತು ದಾರಿಯಲ್ಲಿನ ತೂಕ ನಷ್ಟಕ್ಕಿಂತ ಹೆಚ್ಚಿದ್ದಾಗ ಮಾತ್ರ ದೂರದ ಮಂಡಿಗೆ ಹೋಗುವುದು ಸೂಕ್ತ.",
    callHelperBtn: "ಕಿಸಾನ್ ಮಿತ್ರ ಸಹಾಯವಾಣಿಗೆ ಕರೆ ಮಾಡಿ",
    fieldFeedbackHeading: "ಕ್ಷೇತ್ರ ಮಟ್ಟದ ಪ್ರತಿಕ್ರಿಯೆ ಕಳುಹಿಸಿ",
    farmerNamePlaceholder: "ನಿಮ್ಮ ಹೆಸರು",
    villagePlaceholder: "ನಿಮ್ಮ ಊರು ಅಥವಾ ಮಂಡಿ",
    notesPlaceholder: "ಮಂಡಿಯಲ್ಲಿ ಕಂಡ ಬೆಲೆ ವ್ಯತ್ಯಾಸ ಅಥವಾ ಇತರ ಮಾಹಿತಿ ಬರೆಯಿರಿ",
    sendFeedbackBtn: "ಪ್ರತಿಕ್ರಿಯೆ ಕಳುಹಿಸಿ",

    settingsTitle: "ಅಪ್ಲಿಕೇಶನ್ ಸೆಟ್ಟಿಂಗ್ಸ್",
    textSizeLabel: "ಅಕ್ಷರದ ಗಾತ್ರ",
    textSizeNormal: "ಸಾಮಾನ್ಯ",
    textSizeLarge: "ದೊಡ್ಡದು",
    textSizeXLarge: "ಅತಿ ದೊಡ್ಡದು",
    darkModeLabel: "ಕಪ್ಪು ಹಿನ್ನೆಲೆ (ಡಾರ್ಕ್ ಮೋಡ್)",
    voiceAudioLabel: "ಧ್ವನಿ ಸಹಾಯ",
    startNewFarmerBtn: "ಹೊಸ ರೈತರ ವಿವರ ಪ್ರಾರಂಭಿಸಿ",
    startNewFarmerDesc: "ಹಂಚಿಕೆಯ ಫೋನ್ ಬಳಸುವಾಗ ಹಿಂದಿನ ವಿವರಗಳನ್ನು ತೆರವುಗೊಳಿಸಲು ಇದು ಸಹಕಾರಿ.",
    clearDataBtn: "ಡೇಟಾ ತೆರವುಗೊಳಿಸಿ",
    closeBtn: "ಮುಚ್ಚಿ",

    // Crop Area & Supply Outlook /* needs native review */
    tabCropArea: "ಬೆಳೆ ವಿಸ್ತೀರ್ಣ",
    areaOutlookTitle: "ಬೆಳೆ ವಿಸ್ತೀರ್ಣ ಮತ್ತು ಪೂರೈಕೆ ಮುನ್ನೋಟ",
    areaOutlookSubtitle: "ಜಿಲ್ಲಾ, ರಾಜ್ಯ ಮತ್ತು ರಾಷ್ಟ್ರೀಯ ಈರುಳ್ಳಿ ಬೆಳೆ ವಿಸ್ತೀರ್ಣ ಹಾಗೂ ಬೆಲೆ ಮುನ್ಸೂಚನೆ",
    stepDistrictTitle: "ನಿಮ್ಮ ಜಿಲ್ಲೆ, ಋತು ಮತ್ತು ವರ್ಷ ಆಯ್ಕೆಮಾಡಿ",
    districtLabel: "ಜಿಲ್ಲೆ",
    seasonLabel: "ಋತು",
    yearLabel: "ವರ್ಷ",
    stepAcresTitle: "ನಿಮ್ಮ ಈರುಳ್ಳಿ ಬೆಳೆಯ ವಿಸ್ತೀರ್ಣ ನಮೂದಿಸಿ",
    acresLabel: "ಎಕರೆ",
    hectaresEquivalent: "ಹೆಕ್ಟೇರ್",
    acresLimitHelp: "ಗರಿಷ್ಠ 500 ಎಕರೆಗಳವರೆಗೆ ನಮೂದಿಸಬಹುದು",
    voiceSpeakAcre: "ಧ್ವನಿ ಮೂಲಕ ಎಕರೆ ಹೇಳಿ",
    reportedByYouPrefix: "ನಿಮ್ಮಿಂದ ವರದಿಯಾದ ವಿಸ್ತೀರ್ಣ:",
    stateAreaHeadline: "ಕರ್ನಾಟಕದ ಈ ಋತುವಿನ ಅಧಿಕೃತ ಈರುಳ್ಳಿ ವಿಸ್ತೀರ್ಣ:",
    cardDistrict: "ಜಿಲ್ಲಾ ವಿಸ್ತೀರ್ಣ",
    cardState: "ಕರ್ನಾಟಕ ರಾಜ್ಯ",
    cardCountry: "ಭಾರತ (ರಾಷ್ಟ್ರೀಯ)",
    fiveYearAvg: "5-ವರ್ಷಗಳ ಸರಾಸರಿ",
    signalHigher: "ಹೆಚ್ಚು",
    signalNormal: "ಸಾಮಾನ್ಯ",
    signalLower: "ಕಡಿಮೆ",
    notAvailable: "ಲಭ್ಯವಿಲ್ಲ",
    forecastsDisabledNotice: "ನೈಜ ಬೆಲೆ ಇತಿಹಾಸ ಇನ್ನೂ ಇಲ್ಲ, ಮುನ್ಸೂಚನೆಗಳನ್ನು ನಿಷ್ಕ್ರಿಯಗೊಳಿಸಲಾಗಿದೆ",
    districtNotTrackedDisclaimer: "ಈ ಜಿಲ್ಲೆಗೆ ಅಧಿಕೃತ ವಾಣಿಜ್ಯ ಈರುಳ್ಳಿ ವಿಸ್ತೀರ್ಣ ಡೇಟಾ ಲಭ್ಯವಿಲ್ಲ. ರಾಜ್ಯ ಮಟ್ಟದ ಅಂಕಿಅಂಶಗಳನ್ನು ಪ್ರದರ್ಶಿಸಲಾಗಿದೆ.",
    reportedByFarmersStrip: "ಈ ಜಿಲ್ಲೆಯ ರೈತರಿಂದ ವರದಿಯಾದ ಮಾಹಿತಿ",
    farmerReportsCountLabel: "ವರದಿ ಮಾಡಿದ ರೈತರ ಸಂಖ್ಯೆ:",
    coverageRatioLabel: "ವಿಸ್ತೀರ್ಣ ವ್ಯಾಪ್ತಿ ಅನುಪಾತ:",
    tooFewReportsWarning: "ವಿಶ್ವಾಸಾರ್ಹತೆಗೆ ತುಂಬಾ ಕಡಿಮೆ ವರದಿಗಳು",
    historyChartHeading: "ಕಳೆದ 5 ವರ್ಷಗಳ ಈರುಳ್ಳಿ ವಿಸ್ತೀರ್ಣ ಇತಿಹಾಸ",
    supplyPriceOutlookHeading: "ಪೂರೈಕೆಗೆ ಸಂಬಂಧಿಸಿದ ಬೆಲೆ ಮುನ್ನೋಟ",
    priceExpected30d: "30 ದಿನಗಳ ನಂತರ ನಿರೀಕ್ಷಿತ ಬೆಲೆ:",
    priceExpected60d: "60 ದಿನಗಳ ನಂತರ ನಿರೀಕ್ಷಿತ ಬೆಲೆ:",
    priceExpected90d: "90 ದಿನಗಳ ನಂತರ ನಿರೀಕ್ಷಿತ ಬೆಲೆ:",
    farmerAcreageIsolatedNote: "ಗಮನಿಸಿ: ನಿಮ್ಮ ವೈಯಕ್ತಿಕ ವಿಸ್ತೀರ್ಣವು ಮಾದರಿಯ ಬೆಲೆ ಮುನ್ಸೂಚನೆಯನ್ನು ಬದಲಾಯಿಸುವುದಿಲ್ಲ.",
    officialSourceLabel: "ಅಧಿಕೃತ ಮೂಲ:",
    publishedOnLabel: "ಪ್ರಕಟಣೆ ದಿನಾಂಕ:",
    seeCropAreaBtn: "ಬೆಳೆ ವಿಸ್ತೀರ್ಣ ಮುನ್ನೋಟ ನೋಡಿ",
    backToAdvisorBtn: "ಮಾರಾಟ ಸಲಹೆಗಾರರಿಗೆ ಹಿಂತಿರುಗಿ",
    submitAreaBtn: "ವಿಸ್ತೀರ್ಣ ಸಲ್ಲಿಸಿ ಮುನ್ನೋಟ ನೋಡಿ",

    // Stitch AgroScan Advisor enhancements
    startNewFarmer: "ಹೊಸ ರೈತ",
    navEntry: "ಎಕರೆ ನಮೂದಿಸಿ",
    navResults: "ಪೂರೈಕೆ ಮುನ್ನೋಟ",
    navOfficer: "ಅಧಿಕಾರಿಗಳ ಪರಿಶೀಲನೆ",
    navSources: "ಮೂಲಗಳು ಮತ್ತು ವಿಧಾನ",
    navFeedback: "ಸಹಾಯ ಮತ್ತು ಇತಿಹಾಸ",
    liveKioskConnected: "ಲೈವ್ ಕಿಯೋಸ್ಕ್ ಸಂಪರ್ಕಗೊಂಡಿದೆ (ಮೈಸೂರು ಕಿಯೋಸ್ಕ್ #04)",
    interactiveTestScenarios: "ಪರೀಕ್ಷಾರ್ಥ ಸನ್ನಿವೇಶಗಳು",
    scenarioNormal: "ಸನ್ನಿವೇಶ A: ಸಾಮಾನ್ಯ (ಮೈಸೂರು ಮುಂಗಾರು, 42 ವರದಿಗಳು)",
    scenarioFewReports: "ಸನ್ನಿವೇಶ B: ಕಡಿಮೆ ರೈತರ ವರದಿಗಳು (<30 ಅಥವಾ <5%)",
    scenarioMissingOfficial: "ಸನ್ನಿವೇಶ C: ಅಧಿಕೃತ ರಾಜ್ಯ ಡೇಟಾ ಲಭ್ಯವಿಲ್ಲ",
    scenarioStaleData: "ಸನ್ನಿವೇಶ D: ಹಳೆಯ ಡೇಟಾ ಎಚ್ಚರಿಕೆ (60+ ದಿನಗಳು)",
    scenarioHighSupply: "ಸನ್ನಿವೇಶ E: ಗರಿಷ್ಠ ಪೂರೈಕೆ ಮುನ್ನೋಟ",
    kioskAssistedNote: "ಕಿಯೋಸ್ಕ್ ಸಹಾಯಕ ಮೋಡ್ - ರೈತ ಮತ್ತು ಸಿಬ್ಬಂದಿ ಜಂಟಿ ಓದುವಿಕೆಗೆ ಸೂಕ್ತ.",
    shareWhatsApp: "ವಾಟ್ಸಾಪ್‌ನಲ್ಲಿ ಹಂಚಿಕೊಳ್ಳಿ",
    printPdf: "ಮುದ್ರಿಸಿ / PDF",
    fpoOfficerTitle: "FPO ಅಧಿಕಾರಿ ಪರಿಶೀಲನೆ: ಜಿಲ್ಲಾ ದಾಖಲಾತಿ ಪಟ್ಟಿ",
    fpoOfficerSubtitle: "ಅನಾಮಧೇಯ ಲಾಗ್‌ಗಳು ಮತ್ತು ಗುಣಮಟ್ಟ ಪರಿಶೀಲನೆ",
    exportCsvBtn: "CSV ರಫ್ತು ಮಾಡಿ",
    totalValidSubmissions: "ಒಟ್ಟು ಮಾನ್ಯ ಸಲ್ಲಿಕೆಗಳು",
    flaggedAnomalies: "ಗುರುತಿಸಲಾದ ಅಸಹಜ ನಮೂದುಗಳು",
    sourcesMethodsTitle: "ಪಾರದರ್ಶಕ ವಿಧಾನ ಮತ್ತು ಡೇಟಾ ಮೂಲಗಳು",
    sourcesMethodsSubtitle: "ಪ್ರತಿಯೊಂದು ಸಂಖ್ಯೆಯೂ ಅಧಿಕೃತ ಮೂಲವನ್ನು ಹೊಂದಿದೆ.",
    pillar1Title: "1. ರೈತರ ಮತ್ತು ಅಧಿಕೃತ ಡೇಟಾ ನಡುವೆ ಕಟ್ಟುನಿಟ್ಟಿನ ಪ್ರತ್ಯೇಕತೆ",
    pillar1Desc: "ರೈತರು ನಮೂದಿಸಿದ ವಿಸ್ತೀರ್ಣವನ್ನು ರಾಜ್ಯ ಅಥವಾ ರಾಷ್ಟ್ರೀಯ ಮೊತ್ತಕ್ಕೆ ಎಂದಿಗೂ ಅಂದಾಜಿಸಲಾಗುವುದಿಲ್ಲ. ಅಧಿಕೃತ ಅಂಕಿಅಂಶಗಳು ಕೃಷಿ ಇಲಾಖೆಯಿಂದ ಮಾತ್ರ ಬರುತ್ತವೆ.",
    pillar2Title: "2. ಬೆಲೆಗಳನ್ನು ವ್ಯಾಪ್ತಿಗಳಾಗಿ (Ranges) ತೋರಿಸಲು ಕಾರಣ",
    pillar2Desc: "ಕೃಷಿ ಮಾರುಕಟ್ಟೆಗಳಲ್ಲಿ ಏರಿಳಿತ ಸಹಜ. ಒಂದೇ ನಿಖರ ಸಂಖ್ಯೆ ನೀಡುವುದು ತಪ್ಪಾದ ಭರವಸೆ ನೀಡುತ್ತದೆ. ಆದ್ದರಿಂದ ₹10ಕ್ಕೆ ದುಂಡುಮಾಡಿದ ವ್ಯಾಪ್ತಿಗಳನ್ನು ನೀಡಲಾಗುತ್ತದೆ.",
    pillar3Title: "3. ಬಿತ್ತನೆ ಮತ್ತು ಕಟಾವು ಅವಧಿಯ ಊಹೆಗಳು",
    pillar3Desc: "ಮುಂಗಾರು ಈರುಳ್ಳಿ ನಾಟಿಯಿಂದ ಕಟಾವಿಗೆ 90 ರಿಂದ 105 ದಿನಗಳ ಅವಧಿ ಮತ್ತು 12.5% ಸಾಗಾಣಿಕೆ ನಷ್ಟವನ್ನು ಲೆಕ್ಕಹಾಕಲಾಗುತ್ತದೆ.",
    feedbackHelpfulTitle: "ಈ ಮುನ್ನೋಟ ನಿಮಗೆ ಉಪಯುಕ್ತವಾಯಿತೇ?",
    feedbackHelpfulSubtitle: "ನಿಮ್ಮ ಅನಿಸಿಕೆ ಕರ್ನಾಟಕದ ರೈತರಿಗೆ ಮುನ್ನೋಟ ಸುಧಾರಿಸಲು ಸಹಕಾರಿ.",
    feedbackYes: "ಹೌದು, ಉಪಯುಕ್ತ",
    feedbackNo: "ಇನ್ನಷ್ಟು ಸುಧಾರಣೆ ಬೇಕು",
    recordAudioMemo: "30 ಸೆಕೆಂಡುಗಳ ಧ್ವನಿ ಸಂದೇಶ ರೆಕಾರ್ಡ್ ಮಾಡಿ",
    recentKioskReports: "ಈ ಕಿಯೋಸ್ಕ್‌ನಲ್ಲಿ ದಾಖಲಾದ ಇತ್ತೀಚಿನ ವರದಿಗಳು:",
    staleDataWarningNotice: "ಎಚ್ಚರಿಕೆ: ಅಧಿಕೃತ ಡೇಟಾ ಪ್ರಕಟವಾಗಿ 60 ದಿನಗಳಿಗಿಂತ ಹೆಚ್ಚು ಕಳೆದಿದೆ.",

    // Stitch Farmer Sell Advisor UX System
    stationDepartment: "ಕರ್ನಾಟಕ ಕೃಷಿ ಮಾರುಕಟ್ಟೆ ಇಲಾಖೆ • ICAR-KVK & FPO Network",
    kioskStation: "ಸಾಮೂಹಿಕ ಕಿಯೋಸ್ಕ್ ನಿಲ್ದಾಣ #04 • ರೈತ ಸಂಪರ್ಕ ಕೇಂದ್ರ",
    jointAssistedMode: "ಮಾರಾಟ ನಿರ್ಧಾರ ಸಮಾಲೋಚನೆ",
    jointAssistedSub: "ರೈತ ಮತ್ತು ಕೃಷಿ ಅಧಿಕಾರಿ ಸಮಾಲೋಚನೆ",
    liveMandiMapTitle: "ಸಮೀಪದ ಮಂಡಿಗಳ ಲೈವ್ ನಕ್ಷೆ",
    liveMandiMapRadius: "70 ಕಿ.ಮೀ ವ್ಯಾಪ್ತಿ",
    tempoCalculatorTitle: "ಸಾರಿಗೆ ವೆಚ್ಚ ಅಂದಾಜು (ಟೆಂಪೋ ದರ)",
    tempoVehicleType: "Tata Ace / 1.5 ಟನ್",
    tempoTripEstimate: "ಅಂದಾಜು ಬಾಡಿಗೆ",
    tempoNetGain: "ಸಾರಿಗೆಯ ನಂತರ ನಿವ್ವಳ ಲಾಭ",
    printSlipBtn: "ಮುದ್ರಿಸಿ",
    todayRealization: "ಇಂದಿನ ಸ್ಥಳೀಯ ಮೌಲ್ಯ",
    expectedRealizationWait: "ನಿರೀಕ್ಷಿತ ಮೌಲ್ಯ",
    storageRotAllowance: "ದಾಸ್ತಾನು ಮತ್ತು ಕೊಳೆತ ರಿಸ್ಕ್",
    rotAllowanceDeducted: "~2.5% ಮಾದರಿಯಲ್ಲಿ ಕಳೆಯಲಾಗಿದೆ",
    bestValueBadge: "ಉತ್ತಮ ಲಾಭ (ಶಿಫಾರಸು)",
    highestSpotBadge: "ಗರಿಷ್ಠ ದರ",
    alternativeBadge: "ಪರ್ಯಾಯ ಮಂಡಿ",
    localMandiBadge: "ಸ್ಥಳೀಯ ಮಂಡಿ (ಆಧಾರ)",
    stepReviewSummary: "ತ್ವರಿತ ಸಾರಾಂಶ",
    stepReviewReady: "ಸಿದ್ಧವಾಗಿದೆ",
    stepReviewDirect: "ನೇರ ಲೆಕ್ಕಾಚಾರ",
    liveModalPrice: "ಮಾದರಿ ಬೆಲೆ (Modal)",
    todayArrivals: "ಇಂದಿನ ಆವಕ (Arrival)",
    estimatedLotValue: "ಅಂದಾಜು ಒಟ್ಟು ಮೌಲ್ಯ",
    voiceGuidanceAvailable: "ಧ್ವನಿ ಮಾರ್ಗದರ್ಶನ ಲಭ್ಯವಿದೆ",
    voiceGuidanceSub: "ಕನ್ನಡದಲ್ಲಿ ಬೆಲೆ ಹೋಲಿಕೆಯನ್ನು ಕೇಳಲು ಧ್ವನಿ ಬಟನ್ ಒತ್ತಿ.",
    playAudio: "ಕೇಳಿ",
    youAreHere: "ನೀವು ಇಲ್ಲಿದ್ದೀರಿ",
    distanceMarket: "ದೂರದ ಮಾರುಕಟ್ಟೆ",
    dispatchAdvisory: "ಇಂದಿನ ರವಾನೆ ಸಲಹೆ",
    dispatchAdvisoryText: "ಮಧ್ಯಾಹ್ನ 2 ಗಂಟೆಯೊಳಗೆ ವಾಹನ ಲಭ್ಯತೆ ಉತ್ತಮವಾಗಿದೆ.",
  },

  // ================= HINDI (Pure script - no mixed English/Kannada) =================
  /* needs native review */
  hi: {
    appName: "किसान विक्रय सलाहकार",
    appTagline: "कर्नाटक के प्याज किसानों के लिए निष्पक्ष बाजार मार्गदर्शक",
    tabAdvice: "बिक्री सलाह",
    tabHistory: "मेरा इतिहास",
    tabReliability: "विश्वसनीयता",
    tabHelp: "सहायता",
    settings: "सेटिंग्स",
    online: "ऑनलाइन",
    offline: "ऑफलाइन",

    chooseLanguage: "अपनी भाषा चुनें",
    langKn: "ಕನ್ನಡ",
    langHi: "हिन्दी",
    langEn: "English",

    welcomeTitle: "प्याज बेचने का सही समय और सही मंडी",
    welcomeSubtitle: "मंडी भाव, भाड़ा खर्च और भंडारण का सही हिसाब लगाकर अधिक मुनाफा कमाएं।",
    welcomePromise: "पूरी तरह निशुल्क और पारदर्शी सलाह",
    startBtn: "शुरू करें",

    syntheticBanner: "सिंथेटिक डेटा - वास्तविक निर्णयों के लिए नहीं: यह मॉडल केवल परीक्षण डेटा पर आंका गया है।",
    demoNumbersBadge: "परीक्षण आंकड़े",
    lowConfidenceBadge: "कम विश्वसनीयता",
    lowConfidenceReason: "इस अवधि में बाजार में उतार-चढ़ाव सामान्य से अधिक है। सावधानी से निर्णय लें।",
    staleDataBanner: "पुराना डेटा: अंतिम मंडी रिकॉर्ड {date} का है। कृपया स्थानीय स्तर पर पुष्टि करें।",
    offlineBanner: "इंटरनेट कनेक्शन नहीं है। पहले से सहेजी गई जानकारी दिखाई जा रही है।",
    disclaimer: "यह केवल सलाह है। अंतिम निर्णय पूरी तरह आपका है।",
    sourceMeasured: "वास्तविक दर",
    sourceAssumption: "अनुमानित खर्च",

    stepCounter: "चरण {current} / {total}",
    stepReviewTitle: "जानकारी की जांच",
    nextBtn: "आगे",
    backBtn: "पीछे",
    editLink: "बदलें",
    getAdviceBtn: "सलाह प्राप्त करें",
    calculatingAdvice: "मंडी भाव और सहेजने की लागत जांची जा रही है...",

    stepCropTitle: "आपकी फसल कौन सी है?",
    stepCropDesc: "आज का मंडी पूर्वानुमान देखने के लिए फसल चुनें।",
    cropOnion: "प्याज",
    cropOnionSub: "रबी और खरीफ फसल (सक्रिय मंडी)",
    cropPotato: "आलू",
    cropTomato: "टमाटर",
    comingSoon: "जल्द उपलब्ध",

    stepLocationTitle: "आपकी नजदीकी मंडी कौन सी है?",
    stepLocationDesc: "डीजल और ढुलाई खर्च की गणना के लिए स्थान चुनें।",
    useMyLocation: "मेरा स्थान पहचानें",
    speakVillage: "गांव या मंडी का नाम बोलें",
    listening: "सुन रहे हैं... बोलिए",
    selectMandiPlaceholder: "मंडी चुनें",
    mandiKolar: "कोलार मंडी",
    mandiChikkaballapur: "चिक्काबल्लापुर मंडी",
    mandiYeshwanthpur: "बेंगलुरु यशवंतपुर मंडी",

    stepQuantityTitle: "बिक्री के लिए कितना प्याज तैयार है?",
    stepQuantityDesc: "क्विंटल में कुल मात्रा दर्ज करें।",
    totalVolume: "कुल मात्रा",
    quintalsUnit: "क्विंटल",
    bagConversion: "लगभग {bags} बोरियां (प्रत्येक बोरी 50 किलो)",

    stepStorageTitle: "भंडारण की क्या सुविधा है?",
    stepStorageDesc: "भंडारण की स्थिति से सड़न और वजन में कमी तय होती है।",
    storageNoneTitle: "कोई सुविधा नहीं (खुला स्थान)",
    storageNoneDesc: "जल्दी बेचना सही है। प्रति माह लगभग 12 प्रतिशत वजन कमी।",
    storageWarehouseTitle: "सामान्य गोदाम / शेड",
    storageWarehouseDesc: "हवादार शेड। 15 से 20 दिन तक सुरक्षित रखा जा सकता है।",
    storageColdTitle: "शीत गृह (कोल्ड स्टोरेज)",
    storageColdDesc: "सबसे सुरक्षित। गोदाम रसीद पर ऋण सुविधा उपलब्ध।",
    rotRiskHigh: "सड़ने का भारी जोखिम (0-5 दिन)",
    rotRiskMedium: "मध्यम सुरक्षा (2-3 सप्ताह)",
    rotRiskLow: "न्यूनतम नुकसान (3 महीने तक)",

    stepDebtTitle: "क्या व्यापारी या आढ़ती का बकाया कर्ज है?",
    stepDebtDesc: "क्या आपने मंडी आढ़ती या व्यापारी से अग्रिम रकम ली है?",
    debtNo: "नहीं (कोई कर्ज नहीं)",
    debtNoDesc: "किसी भी मंडी में अपनी मर्जी से बेचने की पूरी आजादी।",
    debtYes: "हाँ (अग्रिम कर्ज है)",
    debtYesDesc: "उसी आढ़ती को फसल सौंपने की मजबूरी हो सकती है।",
    debtPrivate: "बताना नहीं चाहते",
    debtPrivateDesc: "सामान्य अनुमान दिखाया जाएगा।",
    whyWeAskTitle: "हम यह क्यों पूछ रहे हैं?",
    whyWeAskDesc: "आढ़ती का ब्याज ज्यादा होने पर तुरंत बेचना बेहतर है या रोककर रखना, यह गणित समझने के लिए।",

    reviewSummaryHeading: "अपने विवरण की पुष्टि करें",
    reviewCropLabel: "फसल",
    reviewLocationLabel: "लोडिंग मंडी",
    reviewQuantityLabel: "मात्रा",
    reviewStorageLabel: "भंडारण",
    reviewDebtLabel: "व्यापारी कर्ज",

    resultsTitle: "आपके लिए मुख्य सलाह",
    readAloud: "आवाज में सुनें",
    stopVoice: "आवाज रोकें",

    whereToSellTitle: "कहाँ बेचना चाहिए?",
    whereToSellSubtitle: "भाड़ा और आढ़त काटकर आपके हाथ में आने वाली शुद्ध रकम के आधार पर रैंकिंग",
    bestOptionBadge: "सबसे उत्तम विकल्प",
    priceYouMayGet: "आपको मिलने वाली संभावित दर",
    mostLikelyPrice: "सबसे संभावित भाव",
    worstCasePrice: "मंडी गिरने की स्थिति में",
    gainVsLocal: "स्थानीय मंडी से मिलने वाला अतिरिक्त लाभ",
    gainTotalLot: "आपकी पूरी फसल पर कुल अतिरिक्त फायदा",
    costsTakenOffTitle: "काटे गए कुल खर्च (भाड़ा, आढ़त)",
    transportCost: "ढुलाई खर्च",
    mandiFeesCommission: "मंडी शुल्क और हम्माली",
    transitShrinkage: "रास्ते में वजन की कमी",
    localMandiComparisonTitle: "आपकी स्थानीय मंडी (केवल तुलना के लिए)",
    localMandiComparisonDesc: "दूसरी मंडी जाने का भाड़ा खर्च निकालने के बाद फायदा होता है या नहीं, यह जांचने का पैमाना।",

    whenToSellTitle: "कब बेचना चाहिए?",
    whenToSellSubtitle: "आज ही बेचें या कुछ दिन रुकें?",
    sellTodayOption: "आज ही बेचें",
    waitDaysOption: "{days} दिन प्रतीक्षा करें",
    chanceWaitingPays: "रुकने पर अधिक लाभ की संभावना",
    expectedGainWait: "संभावित अतिरिक्त लाभ",
    worstCaseWait: "भाव गिरने पर सबसे खराब स्थिति",

    chartTitle: "भाव का अनुमान (अगले 30 दिन)",
    chartSubtitle: "संभावित कीमतों का दायरा",
    axisPrice: "भाव प्रति क्विंटल (रु.)",
    axisDays: "आज से दिन",
    horizon7d: "7 दिन",
    horizon14d: "14 दिन",
    horizon30d: "30 दिन",
    rangeLegend: "संभावित भाव सीमा",
    medianLegend: "संभावित औसत भाव",

    borrowToggleTitle: "यदि भंडारित माल पर ऋण लें तो?",
    borrowToggleDesc: "गोदाम रसीद पर सस्ता कर्ज मिलने पर निर्णय कैसे बदलता है देखें।",
    borrowActiveStatus: "ऋण सुविधा शामिल की गई",
    borrowWarning: "भाव बढ़ने का लाभ यदि कर्ज के ब्याज से अधिक हो, तभी माल रोकें।",

    storageNearbyTitle: "आसपास के भंडारण केंद्र",
    storageNearbySubtitle: "प्याज को सड़ने से बचाने के विकल्प",
    costPerDay: "प्रति दिन किराया",
    capacityText: "क्षमता उपलब्ध",
    callBtn: "कॉल करें",

    shareWhatsAppBtn: "व्हाट्सएप पर भेजें",
    downloadSummaryBtn: "रिपोर्ट डाउनलोड करें",
    savedToHistoryText: "आपके इतिहास में सहेज लिया गया",
    feedbackPrompt: "क्या यह सलाह आपके काम आई?",
    feedbackHelpful: "हाँ, उपयोगी है",
    feedbackNotHelpful: "नहीं, उपयोगी नहीं है",
    feedbackThankYou: "आपकी राय के लिए धन्यवाद!",

    historyTitle: "पिछली सलाह का रिकॉर्ड",
    historyEmpty: "अभी कोई पुराना रिकॉर्ड नहीं है। होमपेज से सलाह प्राप्त करें।",
    historyAdviceDate: "तारीख",
    historyRecommendedMandi: "सुझाई गई मंडी",
    historyExpectedRange: "संभावित भाव दायरा",
    actualPriceQuestion: "आपको मंडी में वास्तव में क्या भाव मिला?",
    saveActualPriceBtn: "वास्तविक भाव दर्ज करें",
    savedSuccess: "सफलतापूर्वक सहेज लिया गया!",

    reliabilityTitle: "यह सलाह कितनी विश्वसनीय है?",
    reliabilitySubtitle: "हम कभी एक निश्चित भाव का दावा नहीं करते। हर अनुमान के साथ एक दायरा होता है।",
    trafficLightTitle: "पूर्वानुमान सटीकता स्थिति",
    confidenceHigh: "उच्च विश्वसनीयता",
    confidenceMedium: "मध्यम विश्वसनीयता",
    confidenceLow: "कम विश्वसनीयता",
    baselineComparisonTitle: "साधारण अनुमान से तुलना",
    baselineComparisonDesc: "क्या हमारा मॉडल इस साधारण अनुमान से बेहतर है कि 'कल का भाव आज जैसा ही रहेगा'?",
    colHorizon: "समय सीमा",
    colModelError: "मॉडल की औसत त्रुटि",
    colSimpleGuessError: "साधारण अनुमान की त्रुटि",
    colOutcome: "नतीजा",
    beatsSimpleGuess: "मॉडल बेहतर साबित हुआ",
    doesNotBeatSimpleGuess: "साधारण अनुमान ही बेहतर",
    coverageTitle: "दायरा कवरेज (लक्ष्य 70-90%)",
    coverageDesc: "वास्तविक कीमत हमारे बताए दायरे में रहने का प्रतिशत।",
    assumptionsTitle: "मापा गया डेटा बनाम अनुमान",
    assumptionsDesc: "मंडी भाव और मौसम का डेटा रोज मापा जाता है। भाड़ा दर और आढ़त सरकारी नियमों पर आधारित अनुमान हैं।",
    limitsTitle: "मॉडल की ज्ञात सीमाएं",

    helpTitle: "सहायता और संपर्क",
    helpSubtitle: "किसान विक्रय सलाहकार कैसे काम करता है?",
    howItWorksHeading: "तीन सरल कदम",
    step1Text: "1. अपनी मंडी, प्याज की मात्रा और भंडारण की स्थिति बताएं।",
    step2Text: "2. हमारा सिस्टम कोलार, यशवंतपुर और चिक्काबल्लापुर के शुद्ध मुनाफे की तुलना करता है।",
    step3Text: "3. कहाँ और कब बेचना है, यह फैसला आप खुद करें।",
    boundariesHeading: "हमारी सीमाएं और किसान का अधिकार",
    boundariesBody: "हम केवल बाजार विश्लेषण पर आधारित सलाह देते हैं। अंतिम फैसला 100 प्रतिशत आपका ही है।",
    faqHeading: "अक्सर पूछे जाने वाले सवाल",
    faq1Q: "क्या यहाँ दिखाया गया भाव पक्का है?",
    faq1A: "नहीं। मंडी में खुली बोली लगने के कारण भाव में उतार-चढ़ाव होता है। इसलिए हम हमेशा न्यूनतम और अधिकतम सीमा बताते हैं।",
    faq2Q: "दूर की मंडी में जाना कब फायदेमंद होता है?",
    faq2A: "जब दूर की मंडी में मिलने वाला अतिरिक्त भाव रास्ते के भाड़े और वजन कमी से ज्यादा हो, तभी वहां जाना सही है।",
    callHelperBtn: "किसान मित्र हेल्पलाइन पर बात करें",
    fieldFeedbackHeading: "स्थानीय मंडी की जानकारी भेजें",
    farmerNamePlaceholder: "आपका नाम",
    villagePlaceholder: "आपका गांव या मंडी",
    notesPlaceholder: "मंडी में देखा गया भाव या कोई अन्य अनुभव लिखें",
    sendFeedbackBtn: "जानकारी भेजें",

    settingsTitle: "ऐप सेटिंग्स",
    textSizeLabel: "अक्षर का आकार",
    textSizeNormal: "सामान्य",
    textSizeLarge: "बड़ा",
    textSizeXLarge: "बहुत बड़ा",
    darkModeLabel: "डार्क मोड",
    voiceAudioLabel: "आवाज सहायता",
    startNewFarmerBtn: "नए किसान के लिए शुरू करें",
    startNewFarmerDesc: "सांझा फोन इस्तेमाल करते समय पिछला डेटा साफ करने के लिए उपयोगी।",
    clearDataBtn: "डेटा हटाएं",
    closeBtn: "बंद करें",

    // Crop Area & Supply Outlook /* needs native review */
    tabCropArea: "फसल क्षेत्र",
    areaOutlookTitle: "फसल क्षेत्र एवं आपूर्ति दृष्टिकोण",
    areaOutlookSubtitle: "जिला, राज्य और राष्ट्रीय प्याज बुवाई क्षेत्र और मूल्य अनुमान",
    stepDistrictTitle: "अपना जिला, मौसम और वर्ष चुनें",
    districtLabel: "जिला",
    seasonLabel: "मौसम",
    yearLabel: "वर्ष",
    stepAcresTitle: "अपनी प्याज की खेती का रकबा दर्ज करें",
    acresLabel: "एकड़",
    hectaresEquivalent: "हेक्टेयर",
    acresLimitHelp: "अधिकतम 500 एकड़ तक दर्ज किया जा सकता है",
    voiceSpeakAcre: "आवाज से एकड़ बताएं",
    reportedByYouPrefix: "आपके द्वारा दर्ज क्षेत्र:",
    stateAreaHeadline: "कर्नाटक में इस मौसम का आधिकारिक प्याज रकबा:",
    cardDistrict: "जिला क्षेत्र",
    cardState: "कर्नाटक राज्य",
    cardCountry: "भारत (राष्ट्रीय)",
    fiveYearAvg: "5-वर्ष का औसत",
    signalHigher: "अधिक",
    signalNormal: "सामान्य",
    signalLower: "कम",
    notAvailable: "उपलब्ध नहीं",
    forecastsDisabledNotice: "वास्तविक मूल्य इतिहास अभी नहीं है, पूर्वानुमान अक्षम हैं",
    districtNotTrackedDisclaimer: "इस जिले के लिए आधिकारिक वाणिज्यिक प्याज रकबा उपलब्ध नहीं है। राज्य स्तरीय आंकड़े प्रदर्शित हैं।",
    reportedByFarmersStrip: "इस जिले के किसानों द्वारा दर्ज जानकारी",
    farmerReportsCountLabel: "रिपोर्ट करने वाले किसान:",
    coverageRatioLabel: "क्षेत्र कवरेज अनुपात:",
    tooFewReportsWarning: "भरोसे के लिए बहुत कम रिपोर्ट",
    historyChartHeading: "पिछले 5 वर्षों का प्याज रकबा इतिहास",
    supplyPriceOutlookHeading: "आपूर्ति से जुड़ा मूल्य दृष्टिकोण",
    priceExpected30d: "30 दिन बाद अपेक्षित मूल्य:",
    priceExpected60d: "60 दिन बाद अपेक्षित मूल्य:",
    priceExpected90d: "90 दिन बाद अपेक्षित मूल्य:",
    farmerAcreageIsolatedNote: "ध्यान दें: आपका व्यक्तिगत रकबा मॉडल के मूल्य पूर्वानुमान को प्रभावित नहीं करता।",
    officialSourceLabel: "आधिकारिक स्रोत:",
    publishedOnLabel: "प्रकाशन तिथि:",
    seeCropAreaBtn: "फसल रकबा दृष्टिकोण देखें",
    backToAdvisorBtn: "बिक्री सलाहकार पर वापस जाएं",
    submitAreaBtn: "रकबा दर्ज कर दृष्टिकोण देखें",

    // Stitch AgroScan Advisor enhancements
    startNewFarmer: "नया किसान",
    navEntry: "रकबा दर्ज करें",
    navResults: "आपूर्ति दृष्टिकोण",
    navOfficer: "अधिकारी / FPO समीक्षा",
    navSources: "स्रोत और पद्धति",
    navFeedback: "मदद और इतिहास",
    liveKioskConnected: "लाइव कियोस्क कनेक्टेड (मैसूर कियोस्क #04)",
    interactiveTestScenarios: "परीक्षण परिदृश्य",
    scenarioNormal: "परिदृश्य A: सामान्य (मैसूर खरीफ, 42 रिपोर्ट)",
    scenarioFewReports: "परिदृश्य B: कम किसान रिपोर्ट (<30 या <5%)",
    scenarioMissingOfficial: "परिदृश्य C: आधिकारिक राज्य डेटा अनुपलब्ध",
    scenarioStaleData: "परिदृश्य D: पुराना डेटा चेतावनी (60+ दिन)",
    scenarioHighSupply: "परिदृश्य E: अत्यधिक आपूर्ति दृष्टिकोण",
    kioskAssistedNote: "कियोस्क सहायक मोड - किसान और सहायक के साझा पठन हेतु अनुकूलित।",
    shareWhatsApp: "व्हाट्सएप पर साझा करें",
    printPdf: "प्रिंट / PDF",
    fpoOfficerTitle: "FPO अधिकारी समीक्षा: जिला प्रविष्टियां सूची",
    fpoOfficerSubtitle: "अनाम लॉग और गुणवत्ता सत्यापन",
    exportCsvBtn: "CSV निर्यात करें",
    totalValidSubmissions: "कुल मान्य प्रविष्टियां",
    flaggedAnomalies: "संदिग्ध प्रविष्टियां",
    sourcesMethodsTitle: "पारदर्शी पद्धति और डेटा स्रोत",
    sourcesMethodsSubtitle: "प्रत्येक आंकड़े का स्रोत प्रमाणित है।",
    pillar1Title: "1. किसान और आधिकारिक डेटा का पूर्ण पृथक्करण",
    pillar1Desc: "किसानों द्वारा दर्ज रकबे को कभी भी राज्य या राष्ट्रीय योग में नहीं बदला जाता। आधिकारिक आंकड़े केवल कृषि विभाग से लिए जाते हैं।",
    pillar2Title: "2. मूल्य को सीमा (Range) के रूप में दर्शाने का कारण",
    pillar2Desc: "कृषि बाजारों में उतार-चढ़ाव स्वाभाविक है। एकल संख्या देना गलत सटीकता दर्शाता है। इसलिए ₹10 के निकटतम पूर्णांक की सीमा दी जाती है।",
    pillar3Title: "3. बुवाई से कटाई की कृषि संबंधी मान्यताएं",
    pillar3Desc: "खरीफ प्याज की रोपाई से कटाई की अवधि 90 से 105 दिन और 12.5% परिवहन क्षय आंका गया है।",
    feedbackHelpfulTitle: "क्या यह दृष्टिकोण उपयोगी था?",
    feedbackHelpfulSubtitle: "आपकी प्रतिक्रिया कर्नाटक के किसानों के लिए इस सेवा को बेहतर बनाएगी।",
    feedbackYes: "हाँ, उपयोगी है",
    feedbackNo: "सुधार की आवश्यकता",
    recordAudioMemo: "30 सेकंड का ऑडियो नोट रिकॉर्ड करें",
    recentKioskReports: "इस कियोस्क पर हाल की प्रविष्टियां:",
    staleDataWarningNotice: "सूचना: आधिकारिक डेटा 60 से अधिक दिनों पहले प्रकाशित हुआ था।",

    // Stitch Farmer Sell Advisor UX System
    stationDepartment: "कर्नाटक कृषि विपणन विभाग • ICAR-KVK & FPO Network",
    kioskStation: "सामूहिक कियोस्क स्टेशन #04 • रायता संपर्क केंद्र",
    jointAssistedMode: "बिक्री निर्णय परामर्श",
    jointAssistedSub: "किसान और कृषि अधिकारी संयुक्त परामर्श",
    liveMandiMapTitle: "नजदीकी मंडियों का लाइव नक्शा",
    liveMandiMapRadius: "70 किमी दायरा",
    tempoCalculatorTitle: "ढुलाई खर्च का अनुमान (टेंपो किराया)",
    tempoVehicleType: "Tata Ace / 1.5 टन",
    tempoTripEstimate: "अनुमानित किराया",
    tempoNetGain: "ढुलाई के बाद शुद्ध लाभ",
    printSlipBtn: "पर्ची प्रिंट करें",
    todayRealization: "आज का स्थानीय मूल्य",
    expectedRealizationWait: "प्रतीक्षा पर अपेक्षित मूल्य",
    storageRotAllowance: "भंडारण व सड़ांध जोखिम",
    rotAllowanceDeducted: "~2.5% मॉडल में घटाया गया",
    bestValueBadge: "सर्वोत्तम लाभ (अनुशंसित)",
    highestSpotBadge: "अधिकतम मंडी भाव",
    alternativeBadge: "वैकल्पिक मंडी",
    localMandiBadge: "स्थानीय मंडी (आधार)",
    stepReviewSummary: "त्वरित सारांश",
    stepReviewReady: "तैयार है",
    stepReviewDirect: "सीधी गणना",
    liveModalPrice: "मॉडल भाव",
    todayArrivals: "आज की आवक",
    estimatedLotValue: "अनुमानित कुल मूल्य",
    voiceGuidanceAvailable: "ध्वनि मार्गदर्शन उपलब्ध है",
    voiceGuidanceSub: "हिंदी में भाव की तुलना सुनने के लिए स्पीकर दबाएं।",
    playAudio: "सुनें",
    youAreHere: "आप यहाँ हैं",
    distanceMarket: "दूर की मंडी",
    dispatchAdvisory: "आज की लदान सलाह",
    dispatchAdvisoryText: "दोपहर 2 बजे से पहले वाहन उपलब्धता अनुकूल है।",
  },

  // ================= ENGLISH (Pure script - no mixed Indic terms) =================
  en: {
    appName: "Farmer Sell Advisor",
    appTagline: "Decision intelligence for Karnataka smallholder onion farmers",
    tabAdvice: "Advice",
    tabHistory: "My History",
    tabReliability: "How reliable?",
    tabHelp: "Help",
    settings: "Settings",
    online: "Online",
    offline: "Offline",

    chooseLanguage: "Choose your language",
    langKn: "ಕನ್ನಡ",
    langHi: "हिन्दी",
    langEn: "English",

    welcomeTitle: "Where and when to sell your onions",
    welcomeSubtitle: "Compare nearby mandis, freight costs, and storage decay to maximize your take-home cash.",
    welcomePromise: "100% free, honest advice with uncertainty ranges",
    startBtn: "Start",

    syntheticBanner: "SYNTHETIC DATA - NOT FOR REAL DECISIONS: This model was evaluated on generated benchmark rows.",
    demoNumbersBadge: "Demo numbers",
    lowConfidenceBadge: "Low confidence",
    lowConfidenceReason: "Market volatility in this window is higher than normal. Weigh downside risk carefully.",
    staleDataBanner: "Stale data notice: Latest mandi records are from {date}. Verify locally.",
    offlineBanner: "No internet connection. Showing your saved results.",
    disclaimer: "This is advice. The decision is yours.",
    sourceMeasured: "Measured",
    sourceAssumption: "Assumption",

    stepCounter: "Step {current} of {total}",
    stepReviewTitle: "Review your information",
    nextBtn: "Next",
    backBtn: "Back",
    editLink: "Edit",
    getAdviceBtn: "Get advice",
    calculatingAdvice: "Checking mandi clearing prices and logistics...",

    stepCropTitle: "What crop are you selling?",
    stepCropDesc: "Select your harvest variety for today's mandi forecast.",
    cropOnion: "Onion",
    cropOnionSub: "Rabi & Kharif crop (active APMC volume)",
    cropPotato: "Potato",
    cropTomato: "Tomato",
    comingSoon: "Coming soon",

    stepLocationTitle: "Where is your nearest mandi?",
    stepLocationDesc: "Your loading point for calculating diesel and logistics deductions.",
    useMyLocation: "Use my location",
    speakVillage: "Speak village name",
    listening: "Listening... speak now",
    selectMandiPlaceholder: "Select mandi",
    mandiKolar: "Kolar Mandi",
    mandiChikkaballapur: "Chikkaballapur Mandi",
    mandiYeshwanthpur: "Bengaluru Yeshwanthpur Mandi",

    stepQuantityTitle: "How much harvest is ready?",
    stepQuantityDesc: "Enter your total volume in quintals.",
    totalVolume: "Total volume",
    quintalsUnit: "Quintals",
    bagConversion: "about {bags} bags (50 kg gunny bags)",

    stepStorageTitle: "What storage do you have?",
    stepStorageDesc: "Storage conditions determine spoilage and weight loss rates.",
    storageNoneTitle: "None (open farm / field heap)",
    storageNoneDesc: "Fast sale advised. About 12% weight loss per month.",
    storageWarehouseTitle: "Standard farm shed / warehouse",
    storageWarehouseDesc: "Ventilated shed. Safe holding for 15 to 20 days.",
    storageColdTitle: "Controlled cold storage",
    storageColdDesc: "Maximum safety. Eligible for warehouse receipt pledge loans.",
    rotRiskHigh: "High rotting risk (0-5 days)",
    rotRiskMedium: "Moderate protection (2-3 weeks)",
    rotRiskLow: "Minimal loss (up to 3 months)",

    stepDebtTitle: "Do you owe money to a trader?",
    stepDebtDesc: "Did you take advance credit from an APMC commission agent or trader?",
    debtNo: "No (debt free)",
    debtNoDesc: "100% price arbitrage freedom to sell anywhere.",
    debtYes: "Yes (trader advance)",
    debtYesDesc: "You may be obliged to sell through that specific agent.",
    debtPrivate: "Prefer not to say",
    debtPrivateDesc: "Standard market deductions will be shown.",
    whyWeAskTitle: "Why we ask",
    whyWeAskDesc: "If the trader takes high monthly interest, our formula checks if holding stock beats instant farmgate cash.",

    reviewSummaryHeading: "Check your details before getting advice",
    reviewCropLabel: "Crop",
    reviewLocationLabel: "Loading mandi",
    reviewQuantityLabel: "Quantity",
    reviewStorageLabel: "Storage",
    reviewDebtLabel: "Trader advance",

    resultsTitle: "Your Sell Advisor Recommendation",
    readAloud: "Read aloud",
    stopVoice: "Stop voice",

    whereToSellTitle: "Where to sell",
    whereToSellSubtitle: "Nearby markets ranked by what you take home after all costs",
    bestOptionBadge: "Best choice",
    priceYouMayGet: "Price you may get",
    mostLikelyPrice: "most likely about",
    worstCasePrice: "Worst case",
    gainVsLocal: "Gain vs your local mandi",
    gainTotalLot: "Extra for your whole harvest",
    costsTakenOffTitle: "Costs taken off (transport, fees)",
    transportCost: "Transport freight",
    mandiFeesCommission: "Mandi fee & handling",
    transitShrinkage: "Weight loss on the road",
    localMandiComparisonTitle: "Your local mandi (comparison point)",
    localMandiComparisonDesc: "Use this benchmark to see if traveling to other markets covers freight costs.",

    whenToSellTitle: "When to sell",
    whenToSellSubtitle: "Should you sell today or hold?",
    sellTodayOption: "Sell today",
    waitDaysOption: "Hold for {days} days",
    chanceWaitingPays: "Chance waiting pays off",
    expectedGainWait: "Expected extra gain",
    worstCaseWait: "Worst case if prices drop",

    chartTitle: "Price outlook (next 30 days)",
    chartSubtitle: "Estimated price band over time",
    axisPrice: "Price per quintal (Rs)",
    axisDays: "Days from today",
    horizon7d: "7 Days",
    horizon14d: "14 Days",
    horizon30d: "30 Days",
    rangeLegend: "Probable price range",
    medianLegend: "Most likely price",

    borrowToggleTitle: "What if you borrow against stored crop?",
    borrowToggleDesc: "See how the decision shifts with low-interest warehouse receipt financing.",
    borrowActiveStatus: "Pledge credit factored in",
    borrowWarning: "Only store and borrow if expected price gain clearly exceeds loan interest.",

    storageNearbyTitle: "Storage near you",
    storageNearbySubtitle: "Facilities to protect your onions from rotting",
    costPerDay: "Daily rental",
    capacityText: "Capacity available",
    callBtn: "Call",

    shareWhatsAppBtn: "Share on WhatsApp",
    downloadSummaryBtn: "Download summary",
    savedToHistoryText: "Saved to your history",
    feedbackPrompt: "Was this advice helpful?",
    feedbackHelpful: "Helpful",
    feedbackNotHelpful: "Not helpful",
    feedbackThankYou: "Thank you for supporting Karnataka farmers!",

    historyTitle: "Past Advice History",
    historyEmpty: "No previous advice saved yet. Get advice on the home screen.",
    historyAdviceDate: "Date",
    historyRecommendedMandi: "Recommended mandi",
    historyExpectedRange: "Expected price range",
    actualPriceQuestion: "What price did you actually get?",
    saveActualPriceBtn: "Save actual price",
    savedSuccess: "Saved successfully!",

    reliabilityTitle: "How reliable is this advice?",
    reliabilitySubtitle: "We never display a single price as certain. Every forecast states its uncertainty range.",
    trafficLightTitle: "Forecast confidence status",
    confidenceHigh: "High confidence",
    confidenceMedium: "Fair confidence",
    confidenceLow: "Low confidence",
    baselineComparisonTitle: "Comparison against naive baseline",
    baselineComparisonDesc: "Does our ML model outperform the simple guess that 'tomorrow equals today'?",
    colHorizon: "Horizon",
    colModelError: "Our model error",
    colSimpleGuessError: "Simple guess error",
    colOutcome: "Outcome",
    beatsSimpleGuess: "Model beats naive guess",
    doesNotBeatSimpleGuess: "Naive guess is better",
    coverageTitle: "Empirical interval coverage (Target 70–90%)",
    coverageDesc: "Percentage of actual market prices falling within our predicted range.",
    assumptionsTitle: "Assumptions vs measured data",
    assumptionsDesc: "Mandi arrivals and weather are measured daily. Transport diesel and mandi cess are statutory assumptions.",
    limitsTitle: "Known limitations",

    helpTitle: "Help & Support",
    helpSubtitle: "How Farmer Sell Advisor works",
    howItWorksHeading: "Three simple steps",
    step1Text: "1. Tell us your mandi, onion quantity, and storage.",
    step2Text: "2. We compare net realized prices at Kolar, Yeshwanthpur, and Chikkaballapur.",
    step3Text: "3. You make the final call on where and when to sell.",
    boundariesHeading: "Our boundaries & farmer sovereignty",
    boundariesBody: "We advise, you decide. Agricultural markets are volatile and the final decision is 100% yours.",
    faqHeading: "Frequently asked questions",
    faq1Q: "Is the price guaranteed?",
    faq1A: "No. Mandi prices are set by auction and can change daily. That is why we strictly provide a range (P10 to P90), never a guaranteed single number.",
    faq2Q: "When is traveling to a distant mandi worth it?",
    faq2A: "Only when the price spread clearly exceeds transport freight, APMC cess, and weight loss on the road.",
    callHelperBtn: "Call Kisan Mitra Helpline",
    fieldFeedbackHeading: "Send local market observation",
    farmerNamePlaceholder: "Your name",
    villagePlaceholder: "Village or mandi",
    notesPlaceholder: "Observations on local rates or discrepancies",
    sendFeedbackBtn: "Send feedback",

    settingsTitle: "App Settings",
    textSizeLabel: "Text size",
    textSizeNormal: "Normal",
    textSizeLarge: "Large",
    textSizeXLarge: "Extra large",
    darkModeLabel: "Dark mode",
    voiceAudioLabel: "Voice reading",
    startNewFarmerBtn: "Start new farmer session",
    startNewFarmerDesc: "Clears current inputs and history for shared community phones.",
    clearDataBtn: "Clear my data",
    closeBtn: "Close",

    // Crop Area & Supply Outlook
    tabCropArea: "Crop Area",
    areaOutlookTitle: "Crop Area & Supply Outlook",
    areaOutlookSubtitle: "Official onion acreage, farmer reports, and supply-linked price outlook",
    stepDistrictTitle: "Select your district, season, and year",
    districtLabel: "District",
    seasonLabel: "Season",
    yearLabel: "Year",
    stepAcresTitle: "Enter your onion cultivated area",
    acresLabel: "Acres",
    hectaresEquivalent: "Hectares",
    acresLimitHelp: "Maximum 500 acres per single holding report",
    voiceSpeakAcre: "Speak acres by voice",
    reportedByYouPrefix: "Reported by you:",
    stateAreaHeadline: "Karnataka onion area this season:",
    cardDistrict: "District Area",
    cardState: "Karnataka State",
    cardCountry: "India (National)",
    fiveYearAvg: "5-Year Average",
    signalHigher: "Higher",
    signalNormal: "Normal",
    signalLower: "Lower",
    notAvailable: "Not available",
    forecastsDisabledNotice: "No real price history yet, forecasts disabled",
    districtNotTrackedDisclaimer: "Official commercial bulb onion data is not available for this district. Falling back to Karnataka state statistics.",
    reportedByFarmersStrip: "Reported by farmers in this district",
    farmerReportsCountLabel: "Reporting farmers:",
    coverageRatioLabel: "Coverage ratio:",
    tooFewReportsWarning: "Too few reports to trust",
    historyChartHeading: "5-Year Onion Area History",
    supplyPriceOutlookHeading: "Price Outlook Linked to Supply",
    priceExpected30d: "30-day expected price:",
    priceExpected60d: "60-day expected price:",
    priceExpected90d: "90-day expected price:",
    farmerAcreageIsolatedNote: "Notice: Your individual acreage does not alter the model's price forecast.",
    officialSourceLabel: "Official source:",
    publishedOnLabel: "Published:",
    seeCropAreaBtn: "View Crop Area Outlook",
    backToAdvisorBtn: "Back to Sell Advisor",
    submitAreaBtn: "Submit & View Outlook",

    // Stitch AgroScan Advisor enhancements
    startNewFarmer: "New Farmer",
    navEntry: "Enter Acreage",
    navResults: "Supply Outlook",
    navOfficer: "Officer / FPO Review",
    navSources: "Sources & Methods",
    navFeedback: "Help & History",
    liveKioskConnected: "Live Kiosk Connected (Mysuru KVK Kiosk #04)",
    interactiveTestScenarios: "Interactive Test Scenarios",
    scenarioNormal: "Scenario A: Normal (Mysuru Kharif, 42 Reports)",
    scenarioFewReports: "Scenario B: Low Farmer Reports (<30 or <5%)",
    scenarioMissingOfficial: "Scenario C: Official State Data Missing",
    scenarioStaleData: "Scenario D: Stale Data Warning (60+ days)",
    scenarioHighSupply: "Scenario E: Extreme High Supply Outlook",
    kioskAssistedNote: "Kiosk Assisted Mode - Optimized for 1-metre shared reading between farmer & helper.",
    shareWhatsApp: "Share on WhatsApp",
    printPdf: "Print / PDF",
    fpoOfficerTitle: "FPO Officer Review: District Submissions Roster",
    fpoOfficerSubtitle: "Anonymized logs, quality screening & automated anomaly flags",
    exportCsvBtn: "Export Cleaned CSV",
    totalValidSubmissions: "Total Valid Submissions",
    flaggedAnomalies: "Flagged Anomalies",
    sourcesMethodsTitle: "Transparent Methodology & Data Sources",
    sourcesMethodsSubtitle: "Every number in Farmer Sell Advisor carries provenance.",
    pillar1Title: "1. Strict Separation of Farmer & Official Data",
    pillar1Desc: "We never extrapolate individual farmer reports into state or national aggregates. State and national acreages are sourced exclusively from published Directorate of Economics & Statistics bulletins.",
    pillar2Title: "2. Why Prices are Displayed as Rounded Ranges",
    pillar2Desc: "Agriculture markets possess natural volatility. Providing a single point price creates false precision. We round prices to the nearest ₹10 and provide probability bounds.",
    pillar3Title: "3. Explicit Agricultural Assumptions (Labelled)",
    pillar3Desc: "Kharif onion nursery transplantation to harvest is modelled as 90 to 105 days with 12.5% normal post-harvest shrinkage.",
    feedbackHelpfulTitle: "Was This Outlook Helpful?",
    feedbackHelpfulSubtitle: "Your feedback helps improve advice algorithms for Karnataka farmers.",
    feedbackYes: "Yes, Helpful",
    feedbackNo: "Needs Work",
    recordAudioMemo: "Record 30s Audio Note",
    recentKioskReports: "Your Recent Session Reports (Stored on Device):",
    staleDataWarningNotice: "Notice: Official dataset published 60+ days ago.",

    // Stitch Farmer Sell Advisor UX System
    stationDepartment: "Karnataka Agri Marketing Dept • ICAR-KVK & FPO Network",
    kioskStation: "Shared Kiosk Station #04 • Raitha Samparka Kendra",
    jointAssistedMode: "Sell Advisory Consultation",
    jointAssistedSub: "Joint Farmer & Field Staff Assisted Mode",
    liveMandiMapTitle: "Live APMC Spatial Route & Mandi Map",
    liveMandiMapRadius: "70 km Radius",
    tempoCalculatorTitle: "Transport & Fuel Estimator (Tempo Calculator)",
    tempoVehicleType: "Tata Ace / 1.5 Tonne",
    tempoTripEstimate: "Estimated Hire",
    tempoNetGain: "Net gain after transport",
    printSlipBtn: "Print Slip",
    todayRealization: "Today's Local Realization",
    expectedRealizationWait: "Expected Realization After Waiting",
    storageRotAllowance: "Storage & Rot Allowance Risk",
    rotAllowanceDeducted: "~2.5% deducted in model",
    bestValueBadge: "BEST VALUE (Recommended)",
    highestSpotBadge: "HIGHEST SPOT AUCTION",
    alternativeBadge: "ALTERNATIVE MARKET",
    localMandiBadge: "LOCAL MANDI (Baseline)",
    stepReviewSummary: "Batch Summary",
    stepReviewReady: "Ready to calculate",
    stepReviewDirect: "Direct Calculation",
    liveModalPrice: "Modal Price",
    todayArrivals: "Today's Arrivals",
    estimatedLotValue: "Estimated Lot Value",
    voiceGuidanceAvailable: "Voice Guidance Available",
    voiceGuidanceSub: "Tap speaker button to hear advice in plain spoken words.",
    playAudio: "Listen",
    youAreHere: "You are here",
    distanceMarket: "Distant Market",
    dispatchAdvisory: "Today's Dispatch Advisory",
    dispatchAdvisoryText: "Optimal vehicle availability is before 2:00 PM.",
  },
};
