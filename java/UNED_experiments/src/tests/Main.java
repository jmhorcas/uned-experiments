package tests;

import java.nio.file.Path;
import java.nio.file.Paths;

import org.prop4j.Implies;
import org.prop4j.Literal;
import org.prop4j.Node;
import org.prop4j.Not;

import de.ovgu.featureide.fm.core.FeatureModelAnalyzer;
import de.ovgu.featureide.fm.core.analysis.cnf.ClauseList;
import de.ovgu.featureide.fm.core.analysis.cnf.Nodes;
import de.ovgu.featureide.fm.core.analysis.cnf.analysis.CoreDeadAnalysis;
import de.ovgu.featureide.fm.core.analysis.cnf.formula.FeatureModelFormula;
import de.ovgu.featureide.fm.core.analysis.cnf.solver.ISatSolver;
import de.ovgu.featureide.fm.core.analysis.cnf.solver.SimpleSatSolver;
import de.ovgu.featureide.fm.core.analysis.cnf.solver.AdvancedSatSolver;
import de.ovgu.featureide.fm.core.base.IFeatureModel;
import de.ovgu.featureide.fm.core.init.FMCoreLibrary;
import de.ovgu.featureide.fm.core.init.LibraryManager;
import de.ovgu.featureide.fm.core.io.manager.FeatureModelManager;
import splar.core.fm.FeatureModel;
import splar.plugins.reasoners.sat.sat4j.FMReasoningWithSAT;

public class Main {

	public static void main(String[] args) throws Exception {
		LibraryManager.registerLibrary(FMCoreLibrary.getInstance());
		final Path path = Paths.get("models/Pizzas.dimacs");
		final IFeatureModel featureModel = FeatureModelManager.load(path);
		if (featureModel != null) {
			FeatureModelFormula formula = new FeatureModelFormula(featureModel);
			final FeatureModelAnalyzer analyzer = formula.getAnalyzer();
			//analyzer.analyzeFeatureModel(null);
			System.out.println("Feature model is " + (analyzer.isValid(null) ? "not " : "") + "void");
			System.out.println("Core features: " + analyzer.getCoreFeatures(null));
			System.out.println("Dead features: " + analyzer.getDeadFeatures(null));
		} else {
			System.out.println("Feature model could not be read!");
		}
	}

}
