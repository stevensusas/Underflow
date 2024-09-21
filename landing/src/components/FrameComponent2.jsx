import PropTypes from "prop-types";
import styles from "./FrameComponent2.module.css";

const FrameComponent2 = ({ className = "" }) => {
  return (
    <section className={[styles.featuresGridWrapper, className].join(" ")}>
      <div className={styles.featuresGrid}>
        <div className={styles.frameParent}>
          <div className={styles.frameWrapper}>
            <div className={styles.labelParent}>
              <div className={styles.label} />
              <img
                className={styles.materialSymbolsLightmoneyBIcon}
                alt=""
                src="/cb5b9191-81ee-4f56-865d-376ef676f7f3.png"
              />
            </div>
          </div>
          <div className={styles.featureTitles}>
            <div className={styles.costOptimization}>
              <p className={styles.costOptimization1}>{`Cost Optimization `}</p>
            </div>
          </div>
          <div
            className={styles.pickTheCheapest}
          >{`Pick the cheapest, most applicable tech stack `}</div>
        </div>
        <div className={styles.frameGroup}>
          <div className={styles.frameContainer}>
            <div className={styles.ellipseParent}>
              <div className={styles.frameChild} />
              <img
                className={styles.letsIconsserverLight}
                loading="lazy"
                alt=""
                src="/d18a22d4-b224-4002-9a24-12b00d28bb2c.png"
              />
            </div>
          </div>
          <div className={styles.serverManagementWrapper}>
            <div className={styles.serverManagement}>Server Management</div>
          </div>
          <div className={styles.startstopServersBased}>
            Start/stop servers based on usage
          </div>
        </div>
        <div className={styles.frameDiv}>
          <div className={styles.frameWrapper1}>
            <div className={styles.ellipseGroup}>
              <div className={styles.frameItem} />
              <img
                className={styles.uilanalysisIcon}
                loading="lazy"
                alt=""
                src="/b22262c0-de56-493c-89b1-b0dd1d43139b.png"
              />
            </div>
          </div>
          <div className={styles.efficiencyAnalysisWrapper}>
            <div className={styles.efficiencyAnalysis}>Efficiency Analysis</div>
          </div>
          <div className={styles.detailedReportsOn}>
            Detailed reports on runtime + costs
          </div>
        </div>
      </div>
    </section>
  );
};

FrameComponent2.propTypes = {
  className: PropTypes.string,
};

export default FrameComponent2;
