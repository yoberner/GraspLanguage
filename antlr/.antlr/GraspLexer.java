// Generated from /Users/yonatanberner/mygit/GraspLanguage/antlr/Grasp.g4 by ANTLR 4.9.2

    package antlr4;
    // import java.util.HashMap;
    // import edu.yu.compilers.intermediate.symtable.SymTableEntry;
    // import edu.yu.compilers.intermediate.type.Typespec;

import org.antlr.v4.runtime.Lexer;
import org.antlr.v4.runtime.CharStream;
import org.antlr.v4.runtime.Token;
import org.antlr.v4.runtime.TokenStream;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.misc.*;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast"})
public class GraspLexer extends Lexer {
	static { RuntimeMetaData.checkVersion("4.9.2", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		T__0=1, T__1=2, T__2=3, T__3=4, T__4=5, T__5=6, T__6=7, T__7=8, T__8=9, 
		T__9=10, T__10=11, T__11=12, T__12=13, T__13=14, T__14=15, T__15=16, T__16=17, 
		T__17=18, T__18=19, T__19=20, PROGRAM=21, CONST=22, TYPE=23, ARRAY=24, 
		OF=25, RECORD=26, VAR=27, BEGIN=28, END=29, DIV=30, MOD=31, AND=32, OR=33, 
		NOT=34, IF=35, THEN=36, ELSE=37, CASE=38, REPEAT=39, UNTIL=40, WHILE=41, 
		DO=42, FOR=43, TO=44, DOWNTO=45, WRITE=46, WRITELN=47, READ=48, READLN=49, 
		PROCEDURE=50, FUNCTION=51, IDENTIFIER=52, INTEGER=53, REAL=54, NEWLINE=55, 
		WS=56, QUOTE=57, CHARACTER=58, STRING=59, COMMENT=60;
	public static String[] channelNames = {
		"DEFAULT_TOKEN_CHANNEL", "HIDDEN"
	};

	public static String[] modeNames = {
		"DEFAULT_MODE"
	};

	private static String[] makeRuleNames() {
		return new String[] {
			"T__0", "T__1", "T__2", "T__3", "T__4", "T__5", "T__6", "T__7", "T__8", 
			"T__9", "T__10", "T__11", "T__12", "T__13", "T__14", "T__15", "T__16", 
			"T__17", "T__18", "T__19", "A", "B", "C", "D", "E", "F", "G", "H", "I", 
			"J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", 
			"X", "Y", "Z", "PROGRAM", "CONST", "TYPE", "ARRAY", "OF", "RECORD", "VAR", 
			"BEGIN", "END", "DIV", "MOD", "AND", "OR", "NOT", "IF", "THEN", "ELSE", 
			"CASE", "REPEAT", "UNTIL", "WHILE", "DO", "FOR", "TO", "DOWNTO", "WRITE", 
			"WRITELN", "READ", "READLN", "PROCEDURE", "FUNCTION", "IDENTIFIER", "INTEGER", 
			"REAL", "NEWLINE", "WS", "QUOTE", "CHARACTER", "STRING", "CHARACTER_CHAR", 
			"STRING_CHAR", "COMMENT", "COMMENT_CHARACTER"
		};
	}
	public static final String[] ruleNames = makeRuleNames();

	private static String[] makeLiteralNames() {
		return new String[] {
			null, "'.'", "';'", "'('", "','", "')'", "'='", "'-'", "'+'", "'..'", 
			"'['", "']'", "':'", "':='", "'<>'", "'<'", "'<='", "'>'", "'>='", "'*'", 
			"'/'", null, null, null, null, null, null, null, null, null, null, null, 
			null, null, null, null, null, null, null, null, null, null, null, null, 
			null, null, null, null, null, null, null, null, null, null, null, null, 
			null, "'''"
		};
	}
	private static final String[] _LITERAL_NAMES = makeLiteralNames();
	private static String[] makeSymbolicNames() {
		return new String[] {
			null, null, null, null, null, null, null, null, null, null, null, null, 
			null, null, null, null, null, null, null, null, null, "PROGRAM", "CONST", 
			"TYPE", "ARRAY", "OF", "RECORD", "VAR", "BEGIN", "END", "DIV", "MOD", 
			"AND", "OR", "NOT", "IF", "THEN", "ELSE", "CASE", "REPEAT", "UNTIL", 
			"WHILE", "DO", "FOR", "TO", "DOWNTO", "WRITE", "WRITELN", "READ", "READLN", 
			"PROCEDURE", "FUNCTION", "IDENTIFIER", "INTEGER", "REAL", "NEWLINE", 
			"WS", "QUOTE", "CHARACTER", "STRING", "COMMENT"
		};
	}
	private static final String[] _SYMBOLIC_NAMES = makeSymbolicNames();
	public static final Vocabulary VOCABULARY = new VocabularyImpl(_LITERAL_NAMES, _SYMBOLIC_NAMES);

	/**
	 * @deprecated Use {@link #VOCABULARY} instead.
	 */
	@Deprecated
	public static final String[] tokenNames;
	static {
		tokenNames = new String[_SYMBOLIC_NAMES.length];
		for (int i = 0; i < tokenNames.length; i++) {
			tokenNames[i] = VOCABULARY.getLiteralName(i);
			if (tokenNames[i] == null) {
				tokenNames[i] = VOCABULARY.getSymbolicName(i);
			}

			if (tokenNames[i] == null) {
				tokenNames[i] = "<INVALID>";
			}
		}
	}

	@Override
	@Deprecated
	public String[] getTokenNames() {
		return tokenNames;
	}

	@Override

	public Vocabulary getVocabulary() {
		return VOCABULARY;
	}


	public GraspLexer(CharStream input) {
		super(input);
		_interp = new LexerATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}

	@Override
	public String getGrammarFileName() { return "Grasp.g4"; }

	@Override
	public String[] getRuleNames() { return ruleNames; }

	@Override
	public String getSerializedATN() { return _serializedATN; }

	@Override
	public String[] getChannelNames() { return channelNames; }

	@Override
	public String[] getModeNames() { return modeNames; }

	@Override
	public ATN getATN() { return _ATN; }

	public static final String _serializedATN =
		"\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2>\u0211\b\1\4\2\t"+
		"\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13"+
		"\t\13\4\f\t\f\4\r\t\r\4\16\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22"+
		"\4\23\t\23\4\24\t\24\4\25\t\25\4\26\t\26\4\27\t\27\4\30\t\30\4\31\t\31"+
		"\4\32\t\32\4\33\t\33\4\34\t\34\4\35\t\35\4\36\t\36\4\37\t\37\4 \t \4!"+
		"\t!\4\"\t\"\4#\t#\4$\t$\4%\t%\4&\t&\4\'\t\'\4(\t(\4)\t)\4*\t*\4+\t+\4"+
		",\t,\4-\t-\4.\t.\4/\t/\4\60\t\60\4\61\t\61\4\62\t\62\4\63\t\63\4\64\t"+
		"\64\4\65\t\65\4\66\t\66\4\67\t\67\48\t8\49\t9\4:\t:\4;\t;\4<\t<\4=\t="+
		"\4>\t>\4?\t?\4@\t@\4A\tA\4B\tB\4C\tC\4D\tD\4E\tE\4F\tF\4G\tG\4H\tH\4I"+
		"\tI\4J\tJ\4K\tK\4L\tL\4M\tM\4N\tN\4O\tO\4P\tP\4Q\tQ\4R\tR\4S\tS\4T\tT"+
		"\4U\tU\4V\tV\4W\tW\4X\tX\4Y\tY\4Z\tZ\3\2\3\2\3\3\3\3\3\4\3\4\3\5\3\5\3"+
		"\6\3\6\3\7\3\7\3\b\3\b\3\t\3\t\3\n\3\n\3\n\3\13\3\13\3\f\3\f\3\r\3\r\3"+
		"\16\3\16\3\16\3\17\3\17\3\17\3\20\3\20\3\21\3\21\3\21\3\22\3\22\3\23\3"+
		"\23\3\23\3\24\3\24\3\25\3\25\3\26\3\26\3\27\3\27\3\30\3\30\3\31\3\31\3"+
		"\32\3\32\3\33\3\33\3\34\3\34\3\35\3\35\3\36\3\36\3\37\3\37\3 \3 \3!\3"+
		"!\3\"\3\"\3#\3#\3$\3$\3%\3%\3&\3&\3\'\3\'\3(\3(\3)\3)\3*\3*\3+\3+\3,\3"+
		",\3-\3-\3.\3.\3/\3/\3\60\3\60\3\60\3\60\3\60\3\60\3\60\3\60\3\61\3\61"+
		"\3\61\3\61\3\61\3\61\3\62\3\62\3\62\3\62\3\62\3\63\3\63\3\63\3\63\3\63"+
		"\3\63\3\64\3\64\3\64\3\65\3\65\3\65\3\65\3\65\3\65\3\65\3\66\3\66\3\66"+
		"\3\66\3\67\3\67\3\67\3\67\3\67\3\67\38\38\38\38\39\39\39\39\3:\3:\3:\3"+
		":\3;\3;\3;\3;\3<\3<\3<\3=\3=\3=\3=\3>\3>\3>\3?\3?\3?\3?\3?\3@\3@\3@\3"+
		"@\3@\3A\3A\3A\3A\3A\3B\3B\3B\3B\3B\3B\3B\3C\3C\3C\3C\3C\3C\3D\3D\3D\3"+
		"D\3D\3D\3E\3E\3E\3F\3F\3F\3F\3G\3G\3G\3H\3H\3H\3H\3H\3H\3H\3I\3I\3I\3"+
		"I\3I\3I\3J\3J\3J\3J\3J\3J\3J\3J\3K\3K\3K\3K\3K\3L\3L\3L\3L\3L\3L\3L\3"+
		"M\3M\3M\3M\3M\3M\3M\3M\3M\3M\3N\3N\3N\3N\3N\3N\3N\3N\3N\3O\3O\7O\u01c0"+
		"\nO\fO\16O\u01c3\13O\3P\6P\u01c6\nP\rP\16P\u01c7\3Q\3Q\3Q\3Q\3Q\3Q\3Q"+
		"\5Q\u01d1\nQ\3Q\3Q\3Q\3Q\3Q\3Q\3Q\5Q\u01da\nQ\3Q\3Q\5Q\u01de\nQ\3R\5R"+
		"\u01e1\nR\3R\3R\3R\3R\3S\6S\u01e8\nS\rS\16S\u01e9\3S\3S\3T\3T\3U\3U\3"+
		"U\3U\3V\3V\7V\u01f6\nV\fV\16V\u01f9\13V\3V\3V\3W\3W\3X\3X\3X\3X\5X\u0203"+
		"\nX\3Y\3Y\7Y\u0207\nY\fY\16Y\u020a\13Y\3Y\3Y\3Y\3Y\3Z\3Z\2\2[\3\3\5\4"+
		"\7\5\t\6\13\7\r\b\17\t\21\n\23\13\25\f\27\r\31\16\33\17\35\20\37\21!\22"+
		"#\23%\24\'\25)\26+\2-\2/\2\61\2\63\2\65\2\67\29\2;\2=\2?\2A\2C\2E\2G\2"+
		"I\2K\2M\2O\2Q\2S\2U\2W\2Y\2[\2]\2_\27a\30c\31e\32g\33i\34k\35m\36o\37"+
		"q s!u\"w#y${%}&\177\'\u0081(\u0083)\u0085*\u0087+\u0089,\u008b-\u008d"+
		".\u008f/\u0091\60\u0093\61\u0095\62\u0097\63\u0099\64\u009b\65\u009d\66"+
		"\u009f\67\u00a18\u00a39\u00a5:\u00a7;\u00a9<\u00ab=\u00ad\2\u00af\2\u00b1"+
		">\u00b3\2\3\2#\4\2CCcc\4\2DDdd\4\2EEee\4\2FFff\4\2GGgg\4\2HHhh\4\2IIi"+
		"i\4\2JJjj\4\2KKkk\4\2LLll\4\2MMmm\4\2NNnn\4\2OOoo\4\2PPpp\4\2QQqq\4\2"+
		"RRrr\4\2SSss\4\2TTtt\4\2UUuu\4\2VVvv\4\2WWww\4\2XXxx\4\2YYyy\4\2ZZzz\4"+
		"\2[[{{\4\2\\\\||\4\2C\\c|\5\2\62;C\\c|\3\2\62;\4\2--//\4\2\13\13\"\"\3"+
		"\2))\3\2\177\177\2\u01fe\2\3\3\2\2\2\2\5\3\2\2\2\2\7\3\2\2\2\2\t\3\2\2"+
		"\2\2\13\3\2\2\2\2\r\3\2\2\2\2\17\3\2\2\2\2\21\3\2\2\2\2\23\3\2\2\2\2\25"+
		"\3\2\2\2\2\27\3\2\2\2\2\31\3\2\2\2\2\33\3\2\2\2\2\35\3\2\2\2\2\37\3\2"+
		"\2\2\2!\3\2\2\2\2#\3\2\2\2\2%\3\2\2\2\2\'\3\2\2\2\2)\3\2\2\2\2_\3\2\2"+
		"\2\2a\3\2\2\2\2c\3\2\2\2\2e\3\2\2\2\2g\3\2\2\2\2i\3\2\2\2\2k\3\2\2\2\2"+
		"m\3\2\2\2\2o\3\2\2\2\2q\3\2\2\2\2s\3\2\2\2\2u\3\2\2\2\2w\3\2\2\2\2y\3"+
		"\2\2\2\2{\3\2\2\2\2}\3\2\2\2\2\177\3\2\2\2\2\u0081\3\2\2\2\2\u0083\3\2"+
		"\2\2\2\u0085\3\2\2\2\2\u0087\3\2\2\2\2\u0089\3\2\2\2\2\u008b\3\2\2\2\2"+
		"\u008d\3\2\2\2\2\u008f\3\2\2\2\2\u0091\3\2\2\2\2\u0093\3\2\2\2\2\u0095"+
		"\3\2\2\2\2\u0097\3\2\2\2\2\u0099\3\2\2\2\2\u009b\3\2\2\2\2\u009d\3\2\2"+
		"\2\2\u009f\3\2\2\2\2\u00a1\3\2\2\2\2\u00a3\3\2\2\2\2\u00a5\3\2\2\2\2\u00a7"+
		"\3\2\2\2\2\u00a9\3\2\2\2\2\u00ab\3\2\2\2\2\u00b1\3\2\2\2\3\u00b5\3\2\2"+
		"\2\5\u00b7\3\2\2\2\7\u00b9\3\2\2\2\t\u00bb\3\2\2\2\13\u00bd\3\2\2\2\r"+
		"\u00bf\3\2\2\2\17\u00c1\3\2\2\2\21\u00c3\3\2\2\2\23\u00c5\3\2\2\2\25\u00c8"+
		"\3\2\2\2\27\u00ca\3\2\2\2\31\u00cc\3\2\2\2\33\u00ce\3\2\2\2\35\u00d1\3"+
		"\2\2\2\37\u00d4\3\2\2\2!\u00d6\3\2\2\2#\u00d9\3\2\2\2%\u00db\3\2\2\2\'"+
		"\u00de\3\2\2\2)\u00e0\3\2\2\2+\u00e2\3\2\2\2-\u00e4\3\2\2\2/\u00e6\3\2"+
		"\2\2\61\u00e8\3\2\2\2\63\u00ea\3\2\2\2\65\u00ec\3\2\2\2\67\u00ee\3\2\2"+
		"\29\u00f0\3\2\2\2;\u00f2\3\2\2\2=\u00f4\3\2\2\2?\u00f6\3\2\2\2A\u00f8"+
		"\3\2\2\2C\u00fa\3\2\2\2E\u00fc\3\2\2\2G\u00fe\3\2\2\2I\u0100\3\2\2\2K"+
		"\u0102\3\2\2\2M\u0104\3\2\2\2O\u0106\3\2\2\2Q\u0108\3\2\2\2S\u010a\3\2"+
		"\2\2U\u010c\3\2\2\2W\u010e\3\2\2\2Y\u0110\3\2\2\2[\u0112\3\2\2\2]\u0114"+
		"\3\2\2\2_\u0116\3\2\2\2a\u011e\3\2\2\2c\u0124\3\2\2\2e\u0129\3\2\2\2g"+
		"\u012f\3\2\2\2i\u0132\3\2\2\2k\u0139\3\2\2\2m\u013d\3\2\2\2o\u0143\3\2"+
		"\2\2q\u0147\3\2\2\2s\u014b\3\2\2\2u\u014f\3\2\2\2w\u0153\3\2\2\2y\u0156"+
		"\3\2\2\2{\u015a\3\2\2\2}\u015d\3\2\2\2\177\u0162\3\2\2\2\u0081\u0167\3"+
		"\2\2\2\u0083\u016c\3\2\2\2\u0085\u0173\3\2\2\2\u0087\u0179\3\2\2\2\u0089"+
		"\u017f\3\2\2\2\u008b\u0182\3\2\2\2\u008d\u0186\3\2\2\2\u008f\u0189\3\2"+
		"\2\2\u0091\u0190\3\2\2\2\u0093\u0196\3\2\2\2\u0095\u019e\3\2\2\2\u0097"+
		"\u01a3\3\2\2\2\u0099\u01aa\3\2\2\2\u009b\u01b4\3\2\2\2\u009d\u01bd\3\2"+
		"\2\2\u009f\u01c5\3\2\2\2\u00a1\u01dd\3\2\2\2\u00a3\u01e0\3\2\2\2\u00a5"+
		"\u01e7\3\2\2\2\u00a7\u01ed\3\2\2\2\u00a9\u01ef\3\2\2\2\u00ab\u01f3\3\2"+
		"\2\2\u00ad\u01fc\3\2\2\2\u00af\u0202\3\2\2\2\u00b1\u0204\3\2\2\2\u00b3"+
		"\u020f\3\2\2\2\u00b5\u00b6\7\60\2\2\u00b6\4\3\2\2\2\u00b7\u00b8\7=\2\2"+
		"\u00b8\6\3\2\2\2\u00b9\u00ba\7*\2\2\u00ba\b\3\2\2\2\u00bb\u00bc\7.\2\2"+
		"\u00bc\n\3\2\2\2\u00bd\u00be\7+\2\2\u00be\f\3\2\2\2\u00bf\u00c0\7?\2\2"+
		"\u00c0\16\3\2\2\2\u00c1\u00c2\7/\2\2\u00c2\20\3\2\2\2\u00c3\u00c4\7-\2"+
		"\2\u00c4\22\3\2\2\2\u00c5\u00c6\7\60\2\2\u00c6\u00c7\7\60\2\2\u00c7\24"+
		"\3\2\2\2\u00c8\u00c9\7]\2\2\u00c9\26\3\2\2\2\u00ca\u00cb\7_\2\2\u00cb"+
		"\30\3\2\2\2\u00cc\u00cd\7<\2\2\u00cd\32\3\2\2\2\u00ce\u00cf\7<\2\2\u00cf"+
		"\u00d0\7?\2\2\u00d0\34\3\2\2\2\u00d1\u00d2\7>\2\2\u00d2\u00d3\7@\2\2\u00d3"+
		"\36\3\2\2\2\u00d4\u00d5\7>\2\2\u00d5 \3\2\2\2\u00d6\u00d7\7>\2\2\u00d7"+
		"\u00d8\7?\2\2\u00d8\"\3\2\2\2\u00d9\u00da\7@\2\2\u00da$\3\2\2\2\u00db"+
		"\u00dc\7@\2\2\u00dc\u00dd\7?\2\2\u00dd&\3\2\2\2\u00de\u00df\7,\2\2\u00df"+
		"(\3\2\2\2\u00e0\u00e1\7\61\2\2\u00e1*\3\2\2\2\u00e2\u00e3\t\2\2\2\u00e3"+
		",\3\2\2\2\u00e4\u00e5\t\3\2\2\u00e5.\3\2\2\2\u00e6\u00e7\t\4\2\2\u00e7"+
		"\60\3\2\2\2\u00e8\u00e9\t\5\2\2\u00e9\62\3\2\2\2\u00ea\u00eb\t\6\2\2\u00eb"+
		"\64\3\2\2\2\u00ec\u00ed\t\7\2\2\u00ed\66\3\2\2\2\u00ee\u00ef\t\b\2\2\u00ef"+
		"8\3\2\2\2\u00f0\u00f1\t\t\2\2\u00f1:\3\2\2\2\u00f2\u00f3\t\n\2\2\u00f3"+
		"<\3\2\2\2\u00f4\u00f5\t\13\2\2\u00f5>\3\2\2\2\u00f6\u00f7\t\f\2\2\u00f7"+
		"@\3\2\2\2\u00f8\u00f9\t\r\2\2\u00f9B\3\2\2\2\u00fa\u00fb\t\16\2\2\u00fb"+
		"D\3\2\2\2\u00fc\u00fd\t\17\2\2\u00fdF\3\2\2\2\u00fe\u00ff\t\20\2\2\u00ff"+
		"H\3\2\2\2\u0100\u0101\t\21\2\2\u0101J\3\2\2\2\u0102\u0103\t\22\2\2\u0103"+
		"L\3\2\2\2\u0104\u0105\t\23\2\2\u0105N\3\2\2\2\u0106\u0107\t\24\2\2\u0107"+
		"P\3\2\2\2\u0108\u0109\t\25\2\2\u0109R\3\2\2\2\u010a\u010b\t\26\2\2\u010b"+
		"T\3\2\2\2\u010c\u010d\t\27\2\2\u010dV\3\2\2\2\u010e\u010f\t\30\2\2\u010f"+
		"X\3\2\2\2\u0110\u0111\t\31\2\2\u0111Z\3\2\2\2\u0112\u0113\t\32\2\2\u0113"+
		"\\\3\2\2\2\u0114\u0115\t\33\2\2\u0115^\3\2\2\2\u0116\u0117\5I%\2\u0117"+
		"\u0118\5M\'\2\u0118\u0119\5G$\2\u0119\u011a\5\67\34\2\u011a\u011b\5M\'"+
		"\2\u011b\u011c\5+\26\2\u011c\u011d\5C\"\2\u011d`\3\2\2\2\u011e\u011f\5"+
		"/\30\2\u011f\u0120\5G$\2\u0120\u0121\5E#\2\u0121\u0122\5O(\2\u0122\u0123"+
		"\5Q)\2\u0123b\3\2\2\2\u0124\u0125\5Q)\2\u0125\u0126\5[.\2\u0126\u0127"+
		"\5I%\2\u0127\u0128\5\63\32\2\u0128d\3\2\2\2\u0129\u012a\5+\26\2\u012a"+
		"\u012b\5M\'\2\u012b\u012c\5M\'\2\u012c\u012d\5+\26\2\u012d\u012e\5[.\2"+
		"\u012ef\3\2\2\2\u012f\u0130\5G$\2\u0130\u0131\5\65\33\2\u0131h\3\2\2\2"+
		"\u0132\u0133\5M\'\2\u0133\u0134\5\63\32\2\u0134\u0135\5/\30\2\u0135\u0136"+
		"\5G$\2\u0136\u0137\5M\'\2\u0137\u0138\5\61\31\2\u0138j\3\2\2\2\u0139\u013a"+
		"\5U+\2\u013a\u013b\5+\26\2\u013b\u013c\5M\'\2\u013cl\3\2\2\2\u013d\u013e"+
		"\5-\27\2\u013e\u013f\5\63\32\2\u013f\u0140\5\67\34\2\u0140\u0141\5;\36"+
		"\2\u0141\u0142\5E#\2\u0142n\3\2\2\2\u0143\u0144\5\63\32\2\u0144\u0145"+
		"\5E#\2\u0145\u0146\5\61\31\2\u0146p\3\2\2\2\u0147\u0148\5\61\31\2\u0148"+
		"\u0149\5;\36\2\u0149\u014a\5U+\2\u014ar\3\2\2\2\u014b\u014c\5C\"\2\u014c"+
		"\u014d\5G$\2\u014d\u014e\5\61\31\2\u014et\3\2\2\2\u014f\u0150\5+\26\2"+
		"\u0150\u0151\5E#\2\u0151\u0152\5\61\31\2\u0152v\3\2\2\2\u0153\u0154\5"+
		"G$\2\u0154\u0155\5M\'\2\u0155x\3\2\2\2\u0156\u0157\5E#\2\u0157\u0158\5"+
		"G$\2\u0158\u0159\5Q)\2\u0159z\3\2\2\2\u015a\u015b\5;\36\2\u015b\u015c"+
		"\5\65\33\2\u015c|\3\2\2\2\u015d\u015e\5Q)\2\u015e\u015f\59\35\2\u015f"+
		"\u0160\5\63\32\2\u0160\u0161\5E#\2\u0161~\3\2\2\2\u0162\u0163\5\63\32"+
		"\2\u0163\u0164\5A!\2\u0164\u0165\5O(\2\u0165\u0166\5\63\32\2\u0166\u0080"+
		"\3\2\2\2\u0167\u0168\5/\30\2\u0168\u0169\5+\26\2\u0169\u016a\5O(\2\u016a"+
		"\u016b\5\63\32\2\u016b\u0082\3\2\2\2\u016c\u016d\5M\'\2\u016d\u016e\5"+
		"\63\32\2\u016e\u016f\5I%\2\u016f\u0170\5\63\32\2\u0170\u0171\5+\26\2\u0171"+
		"\u0172\5Q)\2\u0172\u0084\3\2\2\2\u0173\u0174\5S*\2\u0174\u0175\5E#\2\u0175"+
		"\u0176\5Q)\2\u0176\u0177\5;\36\2\u0177\u0178\5A!\2\u0178\u0086\3\2\2\2"+
		"\u0179\u017a\5W,\2\u017a\u017b\59\35\2\u017b\u017c\5;\36\2\u017c\u017d"+
		"\5A!\2\u017d\u017e\5\63\32\2\u017e\u0088\3\2\2\2\u017f\u0180\5\61\31\2"+
		"\u0180\u0181\5G$\2\u0181\u008a\3\2\2\2\u0182\u0183\5\65\33\2\u0183\u0184"+
		"\5G$\2\u0184\u0185\5M\'\2\u0185\u008c\3\2\2\2\u0186\u0187\5Q)\2\u0187"+
		"\u0188\5G$\2\u0188\u008e\3\2\2\2\u0189\u018a\5\61\31\2\u018a\u018b\5G"+
		"$\2\u018b\u018c\5W,\2\u018c\u018d\5E#\2\u018d\u018e\5Q)\2\u018e\u018f"+
		"\5G$\2\u018f\u0090\3\2\2\2\u0190\u0191\5W,\2\u0191\u0192\5M\'\2\u0192"+
		"\u0193\5;\36\2\u0193\u0194\5Q)\2\u0194\u0195\5\63\32\2\u0195\u0092\3\2"+
		"\2\2\u0196\u0197\5W,\2\u0197\u0198\5M\'\2\u0198\u0199\5;\36\2\u0199\u019a"+
		"\5Q)\2\u019a\u019b\5\63\32\2\u019b\u019c\5A!\2\u019c\u019d\5E#\2\u019d"+
		"\u0094\3\2\2\2\u019e\u019f\5M\'\2\u019f\u01a0\5\63\32\2\u01a0\u01a1\5"+
		"+\26\2\u01a1\u01a2\5\61\31\2\u01a2\u0096\3\2\2\2\u01a3\u01a4\5M\'\2\u01a4"+
		"\u01a5\5\63\32\2\u01a5\u01a6\5+\26\2\u01a6\u01a7\5\61\31\2\u01a7\u01a8"+
		"\5A!\2\u01a8\u01a9\5E#\2\u01a9\u0098\3\2\2\2\u01aa\u01ab\5I%\2\u01ab\u01ac"+
		"\5M\'\2\u01ac\u01ad\5G$\2\u01ad\u01ae\5/\30\2\u01ae\u01af\5\63\32\2\u01af"+
		"\u01b0\5\61\31\2\u01b0\u01b1\5S*\2\u01b1\u01b2\5M\'\2\u01b2\u01b3\5\63"+
		"\32\2\u01b3\u009a\3\2\2\2\u01b4\u01b5\5\65\33\2\u01b5\u01b6\5S*\2\u01b6"+
		"\u01b7\5E#\2\u01b7\u01b8\5/\30\2\u01b8\u01b9\5Q)\2\u01b9\u01ba\5;\36\2"+
		"\u01ba\u01bb\5G$\2\u01bb\u01bc\5E#\2\u01bc\u009c\3\2\2\2\u01bd\u01c1\t"+
		"\34\2\2\u01be\u01c0\t\35\2\2\u01bf\u01be\3\2\2\2\u01c0\u01c3\3\2\2\2\u01c1"+
		"\u01bf\3\2\2\2\u01c1\u01c2\3\2\2\2\u01c2\u009e\3\2\2\2\u01c3\u01c1\3\2"+
		"\2\2\u01c4\u01c6\t\36\2\2\u01c5\u01c4\3\2\2\2\u01c6\u01c7\3\2\2\2\u01c7"+
		"\u01c5\3\2\2\2\u01c7\u01c8\3\2\2\2\u01c8\u00a0\3\2\2\2\u01c9\u01ca\5\u009f"+
		"P\2\u01ca\u01cb\7\60\2\2\u01cb\u01cc\5\u009fP\2\u01cc\u01de\3\2\2\2\u01cd"+
		"\u01ce\5\u009fP\2\u01ce\u01d0\t\6\2\2\u01cf\u01d1\t\37\2\2\u01d0\u01cf"+
		"\3\2\2\2\u01d0\u01d1\3\2\2\2\u01d1\u01d2\3\2\2\2\u01d2\u01d3\5\u009fP"+
		"\2\u01d3\u01de\3\2\2\2\u01d4\u01d5\5\u009fP\2\u01d5\u01d6\7\60\2\2\u01d6"+
		"\u01d7\5\u009fP\2\u01d7\u01d9\t\6\2\2\u01d8\u01da\t\37\2\2\u01d9\u01d8"+
		"\3\2\2\2\u01d9\u01da\3\2\2\2\u01da\u01db\3\2\2\2\u01db\u01dc\5\u009fP"+
		"\2\u01dc\u01de\3\2\2\2\u01dd\u01c9\3\2\2\2\u01dd\u01cd\3\2\2\2\u01dd\u01d4"+
		"\3\2\2\2\u01de\u00a2\3\2\2\2\u01df\u01e1\7\17\2\2\u01e0\u01df\3\2\2\2"+
		"\u01e0\u01e1\3\2\2\2\u01e1\u01e2\3\2\2\2\u01e2\u01e3\7\f\2\2\u01e3\u01e4"+
		"\3\2\2\2\u01e4\u01e5\bR\2\2\u01e5\u00a4\3\2\2\2\u01e6\u01e8\t \2\2\u01e7"+
		"\u01e6\3\2\2\2\u01e8\u01e9\3\2\2\2\u01e9\u01e7\3\2\2\2\u01e9\u01ea\3\2"+
		"\2\2\u01ea\u01eb\3\2\2\2\u01eb\u01ec\bS\2\2\u01ec\u00a6\3\2\2\2\u01ed"+
		"\u01ee\7)\2\2\u01ee\u00a8\3\2\2\2\u01ef\u01f0\5\u00a7T\2\u01f0\u01f1\5"+
		"\u00adW\2\u01f1\u01f2\5\u00a7T\2\u01f2\u00aa\3\2\2\2\u01f3\u01f7\5\u00a7"+
		"T\2\u01f4\u01f6\5\u00afX\2\u01f5\u01f4\3\2\2\2\u01f6\u01f9\3\2\2\2\u01f7"+
		"\u01f5\3\2\2\2\u01f7\u01f8\3\2\2\2\u01f8\u01fa\3\2\2\2\u01f9\u01f7\3\2"+
		"\2\2\u01fa\u01fb\5\u00a7T\2\u01fb\u00ac\3\2\2\2\u01fc\u01fd\n!\2\2\u01fd"+
		"\u00ae\3\2\2\2\u01fe\u01ff\5\u00a7T\2\u01ff\u0200\5\u00a7T\2\u0200\u0203"+
		"\3\2\2\2\u0201\u0203\n!\2\2\u0202\u01fe\3\2\2\2\u0202\u0201\3\2\2\2\u0203"+
		"\u00b0\3\2\2\2\u0204\u0208\7}\2\2\u0205\u0207\5\u00b3Z\2\u0206\u0205\3"+
		"\2\2\2\u0207\u020a\3\2\2\2\u0208\u0206\3\2\2\2\u0208\u0209\3\2\2\2\u0209"+
		"\u020b\3\2\2\2\u020a\u0208\3\2\2\2\u020b\u020c\7\177\2\2\u020c\u020d\3"+
		"\2\2\2\u020d\u020e\bY\2\2\u020e\u00b2\3\2\2\2\u020f\u0210\n\"\2\2\u0210"+
		"\u00b4\3\2\2\2\r\2\u01c1\u01c7\u01d0\u01d9\u01dd\u01e0\u01e9\u01f7\u0202"+
		"\u0208\3\b\2\2";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}