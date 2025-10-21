import { NextRequest, NextResponse } from 'next/server';
import { spawn } from 'child_process';
import path from 'path';

const PYTHON_BACKEND = process.env.PYTHON_BACKEND_URL || 'http://localhost:8001';

/**
 * ZION 2.8 AI Orchestrator API
 * Integration with AI Master Orchestrator + Round Table Council
 */

// Helper to call Python backend
async function callPythonBackend(endpoint: string, method: string = 'GET', body?: any) {
  try {
    const url = `${PYTHON_BACKEND}${endpoint}`;
    console.log(`[API] Calling backend: ${method} ${url}`);
    
    const options: RequestInit = {
      method,
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      signal: AbortSignal.timeout(10000)
    };

    if (body) {
      options.body = JSON.stringify(body);
    }

    const response = await fetch(url, options);
    
    if (!response.ok) {
      throw new Error(`Backend error: ${response.status}`);
    }

    const data = await response.json();
    console.log(`[API] Backend response for ${endpoint}:`, JSON.stringify(data).slice(0, 200));
    return data;
  } catch (error) {
    console.error(`[API] Python backend call failed: ${endpoint}`, error);
    throw error;
  }
}

// Helper to execute Python script directly
async function executePythonScript(scriptPath: string, args: string[] = []): Promise<any> {
  return new Promise((resolve, reject) => {
    const pythonProcess = spawn('python3', [scriptPath, ...args]);
    
    let output = '';
    let errorOutput = '';

    pythonProcess.stdout.on('data', (data) => {
      output += data.toString();
    });

    pythonProcess.stderr.on('data', (data) => {
      errorOutput += data.toString();
    });

    pythonProcess.on('close', (code) => {
      if (code !== 0) {
        reject(new Error(`Python script failed: ${errorOutput}`));
      } else {
        try {
          // Try to parse JSON output
          const jsonMatch = output.match(/\{[\s\S]*\}/);
          if (jsonMatch) {
            resolve(JSON.parse(jsonMatch[0]));
          } else {
            resolve({ output, raw: true });
          }
        } catch {
          resolve({ output, raw: true });
        }
      }
    });

    pythonProcess.on('error', (error) => {
      reject(error);
    });
  });
}

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const action = searchParams.get('action');

  try {
    switch (action) {
      case 'status':
        return await getOrchestratorStatus();
      
      case 'components':
        return await getAIComponents();
      
      case 'council-status':
        return await getRoundTableStatus();
      
      case 'councilors':
        return await getCouncilors();
      
      case 'metrics':
        return await getSystemMetrics();
      
      default:
        return NextResponse.json({
          success: true,
          message: 'ZION 2.8 AI Orchestrator API',
          endpoints: {
            'GET ?action=status': 'Get orchestrator status',
            'GET ?action=components': 'Get all AI components',
            'GET ?action=council-status': 'Get Round Table Council status',
            'GET ?action=councilors': 'Get all councilors',
            'GET ?action=metrics': 'Get system metrics',
            'POST': 'Execute AI tasks and council decisions'
          }
        });
    }
  } catch (error) {
    console.error('Orchestrator API error:', error);
    return NextResponse.json({
      success: false,
      error: error instanceof Error ? error.message : 'Unknown error',
      timestamp: new Date().toISOString()
    }, { status: 500 });
  }
}

async function getOrchestratorStatus() {
  try {
    // Try Python backend first
    try {
      const data = await callPythonBackend('/api/ai/orchestrator/status');
      return NextResponse.json({
        success: true,
        source: 'python_backend',
        data
      });
    } catch (backendError) {
      // Fallback to direct script execution
      const projectRoot = path.join(process.cwd(), '..');
      const scriptPath = path.join(projectRoot, 'ai', 'zion_ai_master_orchestrator.py');
      
      const result = await executePythonScript(scriptPath, ['--status']);
      
      return NextResponse.json({
        success: true,
        source: 'direct_execution',
        data: result
      });
    }
  } catch (error) {
    return NextResponse.json({
      success: false,
      error: 'Failed to get orchestrator status',
      details: error instanceof Error ? error.message : 'Unknown error'
    }, { status: 500 });
  }
}

async function getAIComponents() {
  try {
    const backendData = await callPythonBackend('/api/ai/orchestrator/components');
    
    // Backend returns { data: { components: {...}, active_components: N, ... } }
    return NextResponse.json({
      success: true,
      data: backendData.data || backendData // Handle both formats
    });
  } catch (error) {
    console.error('Failed to get AI components from backend:', error);
    
    // Return mock data if backend unavailable
    return NextResponse.json({
      success: true,
      data: {
        components: {
          'oracle_ai': { active: false, status: 'initializing', type: 'oracle_ai', performance_score: 0 },
          'cosmic_analyzer': { active: false, status: 'initializing', type: 'cosmic_analyzer', performance_score: 0 },
          'ai_afterburner': { active: false, status: 'initializing', type: 'ai_afterburner', performance_score: 0 },
          'round_table_council': { active: false, status: 'initializing', type: 'round_table_council', performance_score: 0 }
        },
        total_components: 4,
        active_components: 0,
        system_state: 'initializing',
        orchestrator_active: false
      },
      note: 'Backend unavailable, showing default state'
    });
  }
}

async function getRoundTableStatus() {
  try {
    const data = await callPythonBackend('/api/ai/council/status');
    return NextResponse.json({
      success: true,
      data
    });
  } catch (error) {
    // Return council data from Round Table API
    try {
      const councilResponse = await fetch('http://localhost:3007/api/round-table?action=status');
      const councilData = await councilResponse.json();
      
      return NextResponse.json({
        success: true,
        source: 'round_table_api',
        data: councilData.data
      });
    } catch {
      return NextResponse.json({
        success: false,
        error: 'Round Table Council not available'
      }, { status: 503 });
    }
  }
}

async function getCouncilors() {
  try {
    const data = await callPythonBackend('/api/ai/council/councilors');
    return NextResponse.json({
      success: true,
      data
    });
  } catch (error) {
    // Fallback to Round Table API
    try {
      const councilResponse = await fetch('http://localhost:3007/api/round-table?action=councilors');
      const councilData = await councilResponse.json();
      
      return NextResponse.json({
        success: true,
        source: 'round_table_api',
        data: councilData.data
      });
    } catch {
      return NextResponse.json({
        success: false,
        error: 'Councilors not available'
      }, { status: 503 });
    }
  }
}

async function getSystemMetrics() {
  try {
    const data = await callPythonBackend('/api/ai/orchestrator/metrics');
    return NextResponse.json({
      success: true,
      data
    });
  } catch (error) {
    return NextResponse.json({
      success: true,
      data: {
        total_ai_tasks: 0,
        active_components: 0,
        system_performance: 0.0,
        mining_enhancement: 0.0,
        oracle_consensus: 0.0,
        sacred_geometry_bonus: 0.0
      },
      note: 'Backend unavailable, showing default metrics'
    });
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { action, ...params } = body;

    switch (action) {
      case 'start_orchestration':
        return await startOrchestration(params);
      
      case 'convene_council':
        return await conveneCouncil(params);
      
      case 'councilor_task':
        return await executeCouncilorTask(params);
      
      case 'activate_component':
        return await activateComponent(params);
      
      case 'deactivate_component':
        return await deactivateComponent(params);
      
      default:
        return NextResponse.json({
          success: false,
          error: 'Invalid action'
        }, { status: 400 });
    }
  } catch (error) {
    console.error('Orchestrator POST error:', error);
    return NextResponse.json({
      success: false,
      error: error instanceof Error ? error.message : 'Unknown error'
    }, { status: 500 });
  }
}

async function startOrchestration(params: any) {
  try {
    const data = await callPythonBackend('/api/ai/orchestrator/start', 'POST', params);
    return NextResponse.json({
      success: true,
      data
    });
  } catch (error) {
    return NextResponse.json({
      success: false,
      error: 'Failed to start orchestration',
      details: error instanceof Error ? error.message : 'Unknown error'
    }, { status: 500 });
  }
}

async function conveneCouncil(params: any) {
  try {
    const { topic, urgency = 'normal' } = params;
    
    // Try Python backend first
    try {
      const data = await callPythonBackend('/api/ai/council/convene', 'POST', { topic, urgency });
      return NextResponse.json({
        success: true,
        source: 'python_backend',
        data
      });
    } catch (backendError) {
      // Fallback to Round Table API
      const councilResponse = await fetch('http://localhost:3007/api/round-table', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action: 'convene', topic, urgency })
      });
      
      const councilData = await councilResponse.json();
      
      return NextResponse.json({
        success: true,
        source: 'round_table_api',
        data: councilData.data
      });
    }
  } catch (error) {
    return NextResponse.json({
      success: false,
      error: 'Failed to convene council',
      details: error instanceof Error ? error.message : 'Unknown error'
    }, { status: 500 });
  }
}

async function executeCouncilorTask(params: any) {
  try {
    const { councilor, task, task_params = {} } = params;
    
    const data = await callPythonBackend('/api/ai/council/execute', 'POST', {
      councilor,
      task,
      params: task_params
    });
    
    return NextResponse.json({
      success: true,
      data
    });
  } catch (error) {
    return NextResponse.json({
      success: false,
      error: 'Failed to execute councilor task',
      details: error instanceof Error ? error.message : 'Unknown error'
    }, { status: 500 });
  }
}

async function activateComponent(params: any) {
  try {
    const { component } = params;
    
    const data = await callPythonBackend(`/api/ai/orchestrator/activate/${component}`, 'POST');
    
    return NextResponse.json({
      success: true,
      data
    });
  } catch (error) {
    return NextResponse.json({
      success: false,
      error: 'Failed to activate component',
      details: error instanceof Error ? error.message : 'Unknown error'
    }, { status: 500 });
  }
}

async function deactivateComponent(params: any) {
  try {
    const { component } = params;
    
    const data = await callPythonBackend(`/api/ai/orchestrator/deactivate/${component}`, 'POST');
    
    return NextResponse.json({
      success: true,
      data
    });
  } catch (error) {
    return NextResponse.json({
      success: false,
      error: 'Failed to deactivate component',
      details: error instanceof Error ? error.message : 'Unknown error'
    }, { status: 500 });
  }
}
