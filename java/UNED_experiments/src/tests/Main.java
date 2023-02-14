package tests;

import java.nio.file.Path;
import java.nio.file.Paths;

import de.ovgu.featureide.fm.core.FeatureModelAnalyzer;
import de.ovgu.featureide.fm.core.analysis.cnf.formula.FeatureModelFormula;
import de.ovgu.featureide.fm.core.base.IFeatureModel;
import de.ovgu.featureide.fm.core.init.FMCoreLibrary;
import de.ovgu.featureide.fm.core.init.LibraryManager;
import de.ovgu.featureide.fm.core.io.manager.FeatureModelManager;

public class Main {

	public static void main(String[] args) throws Exception {
		LibraryManager.registerLibrary(FMCoreLibrary.getInstance());
		final Path path = Paths.get(args[0]);
		//final Path path = Paths.get("models/Pizzas.dimacs");
		String filename = path.getFileName().toString();
		filename = filename.substring(0, filename.indexOf('.'));
		
		final IFeatureModel featureModel = FeatureModelManager.load(path);
		if (featureModel != null) {
			FeatureModelFormula formula = new FeatureModelFormula(featureModel);
			long startTime = System.nanoTime();
			final FeatureModelAnalyzer analyzer = formula.getAnalyzer();
			//analyzer.analyzeFeatureModel(null);
			//System.out.println("Feature model is " + (analyzer.isValid(null) ? "not " : "") + "void");
			System.out.println("Core features: " + analyzer.getCoreFeatures(null));
			System.out.println("Dead features: " + analyzer.getDeadFeatures(null));
			long elapsedTime = System.nanoTime() - startTime;
			double seconds = elapsedTime / 1e9;
			System.out.println("Model;Tool;SAT-solver;Seconds");
			System.out.println(filename + ";FeatureIDE;Sat4j;" + seconds);
		} else {
			System.out.println("Feature model could not be read!");
		}
	}

}
