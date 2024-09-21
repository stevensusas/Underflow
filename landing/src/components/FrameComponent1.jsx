import PropTypes from "prop-types";
import styles from "./FrameComponent1.module.css";

const FrameComponent1 = ({ className = "" }) => {
  return (
    <section className={[styles.frameParent, className].join(" ")}>
      <div className={styles.topTitleParent}>
        <div className={styles.topTitle}>
          <h1 className={styles.buildScale}>{`Build & scale documentation`}</h1>
          <div className={styles.stackUnderflowHelpsFoundersWrapper}>
            <div className={styles.stackUnderflowHelpsContainer}>
              <p
                className={styles.stackUnderflowHelps}
              >{`Stack Underflow helps founders optimize server costs by selecting the most efficient tech stack, balancing performance and traffic while minimizing expenses, `}</p>
              <p className={styles.evenWithoutA}>
                even without a CS background
              </p>
            </div>
          </div>
        </div>
        <div className={styles.frameWrapper}>
          <button className={styles.rectangleParent}>
            <div className={styles.frameChild} />
            <div className={styles.getStarted}>Get Started</div>
            <div className={styles.weuiarrowOutlinedWrapper}>
              <img
                className={styles.weuiarrowOutlinedIcon}
                alt=""
                src="/eb043088-757f-45d0-aed6-fb4aae773a40_1726936141625583889.png"
              />
            </div>
          </button>
        </div>
      </div>
      <div className={styles.screenshot20240921At104Parent}>
        <img
          className={styles.screenshot20240921At104}
          loading="lazy"
          alt=""
          src="/8aef1fd6-2667-4091-b4a3-c1aa04d15829.png"
        />
        <div className={styles.filtersHeaderParent}>
          <button className={styles.filtersHeader}>
            <div className={styles.filtersHeaderChild} />
            <div className={styles.readDocumentation}>Read Documentation</div>
          </button>
          <div className={styles.labelParent}>
            <div className={styles.label} />
            <img
              className={styles.screenshot20240921At1041}
              loading="lazy"
              alt=""
              src="/53781d94-2a74-4738-ac7c-15d677c7141a.png"
            />
          </div>
        </div>
      </div>
    </section>
  );
};

FrameComponent1.propTypes = {
  className: PropTypes.string,
};

export default FrameComponent1;
