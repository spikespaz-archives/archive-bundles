import { Ajax } from "ajax";


export const CLOSURE_API = "closure-compiler.appspot.com";

export const DEFAULT_OPTIONS = {
    compilation_level: "SIMPLE_OPTIMIZATIONS", // WHITESPACE_ONLY, SIMPLE_OPTIMIZATIONS, ADVANCED_OPTIMIZATIONS
    output_info: "compiled_code", // compiled_code, warnings, errors, statistics
    output_format: "text" // text, json, xml
};


export class Closure {
    constructor(compilationLevel=DEFAULT_OPTIONS.compilation_level,
                outputInfo=DEFAULT_OPTIONS.output_info,
                outputFormat=DEFAULT_OPTIONS.output_format) {
        this.options = {
            compilation_level: compilationLevel,
            output_info: outputInfo,
            output_format: outputFormat
        };

        this.ajax = new Ajax();

        this.requests = [];
    }

    compile(jsCode="", codeURL="") {
        let options = this.options;

        this.options.js_code = jsCode;
        this.options.code_url = codeURL;

        let request = this.ajax.POST(CLOSURE_API + "/compile", options);
        request.responseJSON = JSON.parse(request.responseText);

        this.requests.push(request);

        return request;
    }

    getCompiled(jsCode="", codeURL="") {
        return this.compile(jsCode, codeURL).responseText;
    }
}